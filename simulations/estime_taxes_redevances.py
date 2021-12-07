import pandas  # noqa: I201
import time

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100
from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# CONFIGURATION

data_period = 2019
# Camino, export Titres miniers et autorisations :
csv_communes = "/Volumes/Transcend2/beta/camino_2020/20201103-12h35-camino-titres-66.csv"
# Camino, export Activités
csv_activites = "/Volumes/Transcend2/beta/camino_2020/20201103-12h42-camino-activites-53.csv"

# ADAPT INPUT DATA

communes_par_titre : pandas.DataFrame = pandas.read_csv(csv_communes)
activite_par_titre : pandas.DataFrame = pandas.read_csv(csv_activites)

filtre_annee_activite = activite_par_titre['annee'] == data_period
activites_data = activite_par_titre[filtre_annee_activite]
titres_ids = activites_data.titre_id

# selection des communes des titres pour lesquels nous avons des activités
# 'titre_id' des exports d'activités (csv_activites) = 'id' des exports de titres (csv_communes)
filtre_titres = communes_par_titre['id'].isin(titres_ids.tolist())
communes_data = communes_par_titre[filtre_titres][
  ['id', 'substances',
  'titulaires_noms', 'titulaires_adresses',
  'communes', 'departements'
  ]
]
communes_ids = communes_data.communes

# simulation_data = pandas.merge(activites_data, communes_data, on=['id'])
# print(simulation_data)

# SIMULATION

def build_simulation(tax_benefit_system, period, titres_ids, communes_ids):
  simulation_builder = SimulationBuilder()
  simulation_builder.create_entities(tax_benefit_system)
  simulation_builder.declare_person_entity('societe', titres_ids)

  # associer communes et titres
  commune_instance = simulation_builder.declare_entity('commune', communes_ids)
  titres_des_communes = communes_ids  # un id par titre existant
  titres_communes_roles = ['societe'] * len(titres_des_communes)  # role de chaque titre dans la commune = societe
  simulation_builder.join_with_persons(commune_instance, titres_des_communes, roles = titres_communes_roles)

  return simulation_builder.build(tax_benefit_system)


def set_simulation_inputs(simulation, openfisca_to_data_keys):
  for k, v in activite_par_titre_keys.items():
    simulation.set_input(k, data_period, activites_data[v])
  return simulation


simulation_period = '2020'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()
current_parameters = tax_benefit_system.parameters(simulation_period)
simulation = build_simulation(tax_benefit_system, simulation_period, titres_ids, communes_ids)

activite_par_titre_keys = {'quantite_aurifere_kg': 'renseignements_orNet'}
simulation = set_simulation_inputs(simulation, activite_par_titre_keys)

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

estimations = titres_ids
resultat = pandas.DataFrame(estimations, columns = colonnes)

resultat['communes'] = communes_data.communes
resultat['titulaires_noms'] = communes_data.titulaires_noms
resultat['titulaires_adresses'] = communes_data.titulaires_adresses
# Base des redevances :
resultat['renseignements_orNet'] = activites_data.renseignements_orNet
# Redevance départementale :
resultat['tarifs_rdm'] = [rdm_tarif_aurifere] * len(titres_ids)
resultat['redevance_departementale_des_mines_aurifere_kg'] = redevance_departementale_des_mines_aurifere_kg
# Redevance communale :
resultat['tarifs_rcm'] = [rcm_tarif_aurifere] * len(titres_ids)
resultat['redevance_communale_des_mines_aurifere_kg'] = redevance_communale_des_mines_aurifere_kg
# Taxe minière sur l'or de Guyane :
resultat['taxe_tarif_pme'] = taxe_tarif_pme
resultat['taxe_tarif_autres'] = taxe_tarif_autres_entreprises
resultat['taxe_guyane_brute'] = taxe_guyane_brute

timestamp = time.strftime("%Y%m%d-%H%M%S")
resultat.to_csv(f'estimation_{timestamp}.csv', index=False)
