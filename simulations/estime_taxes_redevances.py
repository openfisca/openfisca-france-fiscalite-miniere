import pandas  # noqa: I201
import numpy
import time
import re

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100
from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# CONFIGURATION

data_period = 2019

# Camino, export Titres miniers et autorisations :
csv_titres = "/Volumes/Transcend2/beta/camino_2020/data/20201116-22h32-camino-titres-1878.csv"
# Camino, export Activités
# substance "or", tout type de titre, tout statut de titre
# tout type de rapport, statut "déposé" uniquement
# année N-1
csv_activites = "/Volumes/Transcend2/beta/camino_2020/data/20201116-22h30-camino-activites-573.csv"

# ADAPT INPUT DATA

def get_activites_data(csv_activites):
    activite_par_titre : pandas.DataFrame = pandas.read_csv(csv_activites)

    filtre_annee_activite = activite_par_titre['annee'] == data_period
    activites_data = activite_par_titre[filtre_annee_activite][
        ['titre_id', 'annee', 'periode', 'type',
          'renseignements_orBrut', 'renseignements_orNet',
          'renseignements_environnement',
          'complement_texte'
        ]
    ]

    print(len(activites_data), "ACTIVITES")
    print(activites_data[['titre_id', 'annee']].head())

    return activites_data


# titres_ids = titres pour lesquels nous avons des activités
def get_titres_data(csv_titres, titres_ids):
    communes_par_titre : pandas.DataFrame = pandas.read_csv(csv_titres)

    # 'titre_id' des exports d'activités (csv_activites) = 'id' des exports de titres (csv_titres)
    filtre_titres = communes_par_titre['id'].isin(titres_ids.tolist())
    titres_data = communes_par_titre[filtre_titres][
        ['id', 'domaine', 'substances',
          'communes', 'departements', 'administrations_noms',
          'titulaires_noms', 'titulaires_adresses', 'titulaires_categorie',
          'amodiataires_noms', 'amodiataires_adresses', 'amodiataires_categorie'
        ]
    ]

    print(len(titres_data), "TITRES")
    print(titres_data[['id', 'communes']].head())

    return titres_data


def get_simulation_full_data(titres_data, activites_data):
    full_data : pandas.DataFrame = pandas.merge(
        activites_data, titres_data, left_on='titre_id', right_on='id'
        ).drop(columns=['id'])  # on supprime la colonne 'id' en doublon avec 'titre_id'

    print(len(full_data), "SIMULATION DATA")
    # print(full_data[['titre_id', 'periode', 'communes']].head())

    # print(full_data.loc[full_data['titre_id'] == 'm-ax-berge-conrad-2016'][['periode', 'renseignements_environnement']])
    # full_data.to_csv(f'full_data_{time.strftime("%Y%m%d-%H%M%S")}.csv', index=False)

    return full_data


def multi_communes(communes_value):
    return communes_value.str.contains(r';')


def separe_commune_surface(commune_surface):
    '''Transforme ('Commune1 ', '0.123') en 'Commune1', 0.123'''
    match = re.match("(.*)\((.*)\)", commune_surface)  # noqa: W605
    return match.group(1).strip(), match.group(2).strip()


def detect_communes_surfaces(communes_surfaces):
    communes_surfaces_list = communes_surfaces.split(';')
    communes_surfaces_dict = {}
    for item in communes_surfaces_list:
        k, v = separe_commune_surface(item)
        communes_surfaces_dict.update({k: v})

    return communes_surfaces_dict


def rename_titres_multicommunes(data):
    titres_names, titres_occurrences = numpy.unique(data.titre_id, return_counts=True)
    for index, occurrence_titre in enumerate(titres_occurrences):
        if occurrence_titre > 1:
            titre_multicommunes = titres_names[index]
            print("🔴 ", titre_multicommunes)
            titre_multicommunes_df = data[data.titre_id == titre_multicommunes]
            
            for j, row in titre_multicommunes_df.iterrows():
                # row_to_update = data.loc[j]
                print(data.loc[j, 'titre_id'])
                commune, surface = separe_commune_surface(row.communes)
                print(commune)
                data.loc[j, 'titre_id'] += "+" + commune
                print("après", data.loc[j, 'titre_id'])


def clean_data(data):
    une_ligne_par_titre = data[
        # supprime les rapports trimestriels
        (data.periode == 'année')
        # supprime les rapports qui n'ont pas pour objet la production
        & (data.renseignements_orNet.notnull())
        ]

    # print(len(une_ligne_par_titre), "une_ligne_par_titre (via année)")
    # print(une_ligne_par_titre.head())

    quantites_chiffrees = une_ligne_par_titre
    quantites_chiffrees.renseignements_orNet = une_ligne_par_titre.renseignements_orNet.fillna(0.)

    print(len(quantites_chiffrees), "CLEANED DATA")
    # print(quantites_chiffrees[['titre_id', 'periode', 'communes', 'renseignements_orNet']].head())

    # on éclate les titres multicommunaux en une ligne par titre+commune unique
    # attention : on refait l'index du dataframe pour distinguer les lignes résultat.
    quantites_chiffrees.communes = quantites_chiffrees.communes.str.split(pat=';')
    une_commune_par_titre = quantites_chiffrees.explode("communes", ignore_index=True)  # ! pandas v 1.1.0+

    rename_titres_multicommunes(une_commune_par_titre)
    return une_commune_par_titre


activites_data = get_activites_data(csv_activites)
titres_ids = activites_data.titre_id  # selection des titres pour lesquels nous avons des activités
titres_data = get_titres_data(csv_titres, titres_ids)

full_data = get_simulation_full_data(titres_data, activites_data)
data = clean_data(full_data)  # titres ayant des rapports annuels d'activité citant la production
cleaned_titres_ids = data.titre_id


# SIMULATION

def build_simulation(tax_benefit_system, period, titres_ids, communes_ids):
  simulation_builder = SimulationBuilder()
  simulation_builder.create_entities(tax_benefit_system)
  simulation_builder.declare_person_entity('societe', titres_ids)  # TODO titres sans doublons ?

  # associer les communes aux titres
  commune_instance = simulation_builder.declare_entity('commune', communes_ids)
  titres_des_communes = communes_ids  # un id par titre existant dans l'ordre de titres_ids
  titres_communes_roles = ['societe'] * len(titres_des_communes)  # role de chaque titre dans la commune = societe
  simulation_builder.join_with_persons(commune_instance, titres_des_communes, roles = titres_communes_roles)

  return simulation_builder.build(tax_benefit_system)


def set_simulation_inputs(simulation, data, openfisca_to_data_keys):
  for k, v in activite_par_titre_keys.items():
    simulation.set_input(k, data_period, data[v])
  return simulation


simulation_period = '2020'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()
current_parameters = tax_benefit_system.parameters(simulation_period)

simulation = build_simulation(
  tax_benefit_system, simulation_period,
  data.titre_id, data.communes
  )

# cleaned_titres_ids = simulation.populations['societe'].ids
simulation_societes = simulation.populations['societe'].ids
simulation_communes = simulation.populations['commune'].ids

# print(len(simulation_societes))
# societes_names, societes_occurrences = numpy.unique(simulation_societes, return_counts=True)
# for index, item in enumerate(societes_occurrences):
#   if item > 1:
#     print("societe en doublon", societes_names[index])
# print(len(simulation_communes))
# print(numpy.unique(simulation_communes, return_counts=True))

activite_par_titre_keys = {'quantite_aurifere_kg': 'renseignements_orNet'}
simulation = set_simulation_inputs(simulation, data, activite_par_titre_keys)

rdm_tarif_aurifere = current_parameters.redevances.departementales.aurifere
rcm_tarif_aurifere = current_parameters.redevances.communales.aurifere

redevance_departementale_des_mines_aurifere_kg = simulation.calculate('redevance_departementale_des_mines_aurifere_kg', simulation_period)
redevance_communale_des_mines_aurifere_kg = simulation.calculate('redevance_communale_des_mines_aurifere_kg', simulation_period)

taxe_tarif_pme = current_parameters.taxes.guyane.categories.pme
taxe_tarif_autres_entreprises = current_parameters.taxes.guyane.categories.autre
taxe_guyane_brute = simulation.calculate('taxe_guyane_brute', simulation_period)

# SIMULATION OUTPUT

# TODO ordonnancer par titres
colonnes = [
  'titre_id', 'communes',
  'titulaires_noms', 'titulaires_adresses',
  # Base des redevances :
  'substances', 'renseignements_orNet',
  # Redevance départementale :
  'tarifs_rdm',
  'redevance_departementale_des_mines_aurifere_kg',
  # Redevance communale :
  'tarifs_rcm',
  'redevance_communale_des_mines_aurifere_kg',
  # Taxe minière sur l'or de Guyane :
  'taxe_tarif_pme',
  'taxe_tarif_autres',
  'taxe_guyane_brute'
  ]

resultat = pandas.DataFrame(data, columns = colonnes)

resultat['communes'] = titres_data.communes
resultat['titulaires_noms'] = titres_data.titulaires_noms
resultat['titulaires_adresses'] = titres_data.titulaires_adresses
# Base des redevances :
resultat['renseignements_orNet'] = activites_data.renseignements_orNet
# Redevance départementale :
resultat['tarifs_rdm'] = [rdm_tarif_aurifere] * len(cleaned_titres_ids)
resultat['redevance_departementale_des_mines_aurifere_kg'] = redevance_departementale_des_mines_aurifere_kg
# Redevance communale :
resultat['tarifs_rcm'] = [rcm_tarif_aurifere] * len(cleaned_titres_ids)
resultat['redevance_communale_des_mines_aurifere_kg'] = redevance_communale_des_mines_aurifere_kg
# Taxe minière sur l'or de Guyane :
resultat['taxe_tarif_pme'] = taxe_tarif_pme
resultat['taxe_tarif_autres'] = taxe_tarif_autres_entreprises
resultat['taxe_guyane_brute'] = taxe_guyane_brute

timestamp = time.strftime("%Y%m%d-%H%M%S")
# resultat.to_csv(f'matrice_drfip_{timestamp}.csv', index=False)
# TODO Vérifier quels titres du fichier CSV en entrée ne sont pas dans le rapport final.
