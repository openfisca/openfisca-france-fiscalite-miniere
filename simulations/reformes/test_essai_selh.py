# INSTALL : make install; pip install pandas
import re

import numpy as np  # noqa: I201
import pandas  # noqa: I201

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100

from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# Simulation d'une réforme de répartition communale de la Redevance Communale
# des Mines (RCM) pour les exploitations de sel en dissolution :
# pour chaque concession (titre) d'une mine, évaluation de la distribution
# de la production et du produit de la taxe au prorata de la surface du titre
# sur chaque commune.
# (Appliquée aux données de la région Grand-Est.)

# CONFIGURATION
# -------------

path_data_titres = './data_titres.csv'
path_data_activites = './data_activites.csv'

# LECTURE DES DONNEES
# -------------------


def separe_commune_surface(commune_surface):
    '''Transforme [('Commune1 ', '0.123')] en { 'Commune1': 0.123 }'''

    match = re.match("(.*)\((.*)\)", commune_surface)  # noqa: W605
    return {match.group(1).strip(): match.group(2).strip()}


# DONNEES TITRES


titres = pandas.read_csv(path_data_titres)
# pour un titre, communes et leurs surfaces couvertes
# ['id', 'nom', 'type', 'domaine', 'date_debut', 'date_fin',
#        'date_demande', 'statut', 'volume', 'volume_unite', 'substances',
#        'surface_km2', 'communes', 'departements', 'regions',
#        'administrations_noms', 'titulaires_noms', 'titulaires_adresses',
#        'titulaires_legal', 'amodiataires_noms', 'amodiataires_adresses',
#        'amodiataires_legal', 'geojson', 'engagement', 'engagement_devise',
#        'reference_DEB', 'reference_RNTM']
titres_ids = titres.id
titres_multicommunes = titres.communes  # "Commune1 (0.123);Commune2 (0.456)"

communes_ids = []
# Pour chaque titre, parse le contenu de la colonne 'communes'
# et le rempace par un dictionnaire
for index, communes_surfaces in titres_multicommunes.items():
    liste_communes_surfaces = communes_surfaces.split(';')
    dict_communes_surfaces = {}
    for i in liste_communes_surfaces:
        dict_communes_surfaces.update(separe_commune_surface(i))
    titres.communes.at[index] = dict_communes_surfaces
    communes_ids.extend(dict_communes_surfaces.keys())

# Suppression des doublons
communes_ids = np.unique(communes_ids)


# DONNEES ACTIVITES


activites = pandas.read_csv(path_data_activites)
# productions
# ["id","titre_id","type","statut","annee","periode","frequence_periode_id",
#  "renseignements_selh","renseignements_selg","complement_texte"]

# DOCUMENTATION
# noms code minier = noms dans le décret des taux de redevances
# selh = sel en dissolution (en référence à H2O)
# selr = sel raffiné
# selg = sel par abattage (en référence au sel gemme extrait par abattage)


filtre_selh = activites['renseignements_selh'] != ""
activites_selh = activites[filtre_selh]

filtre_2018 = activites_selh['annee'] == 2018
activites_selh_2018 = activites_selh[filtre_2018]

activite_selh_2018_par_titre = pandas.merge(
    titres,
    activites_selh_2018,
    left_on="id",
    right_on="titre_id")
activite_selh_2018_par_titre['renseignements_selh'].fillna(0, inplace=True)
print(activite_selh_2018_par_titre[[  # noqa: T201
    'id_x', 'communes', 'renseignements_selh', 'annee'
    ]])


# SIMULATION : CAS ACTUEL
# -----------------------

period = '2019'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()

simulation_builder = SimulationBuilder()
simulation_builder.create_entities(tax_benefit_system)
simulation_builder.declare_person_entity('article', titres_ids)

simulation = simulation_builder.build(tax_benefit_system)
simulation.set_input(
    'quantite_sel_dissolution_kt', '2018',
    activite_selh_2018_par_titre['renseignements_selh']
    )

redevance_communale_des_mines_sel_dissolution_kt = simulation.calculate(
    'redevance_communale_des_mines_sel_dissolution_kt', period
    )
print("redevance_communale_des_mines_sel_dissolution_kt ?")  # noqa: T201
print(redevance_communale_des_mines_sel_dissolution_kt)  # noqa: T201


# SIMULATION : ESSAI REFORME
# --------------------------

# Si j’ai le titre Choupinou sur les communes A et B.
# Sachant qu'il est géographiquement situé sur x Km2 de A et y Km2 de B.
# Si le titre Choupinou paie :moneybag: aujourd’hui à l’Etat,
# demain il pourrait payer : :moneybag: * x / (x+y) à A et :moneybag: * y / (x+y) à B.


# "Commune", "redevance communale totale pour la commune",
# "[titreA (redevance communale pour toutes les substances
#               de ce titre sur cette commune);
#   titreB (redevance communale pour toutes les substances
#               de cet autre titre) ]"
data_reforme = []
colonnes = [
    'commune',
    'redevance communale totale',
    'titre',
    'redevance communale par titre']

for index, row in activite_selh_2018_par_titre.iterrows():
    print("\n", row.id_x)  # noqa: T201
    titre_communes = row.communes

    titre_surface_totale = sum(map(float, titre_communes.values()))
    print(titre_surface_totale, " = ", titre_communes)  # noqa: T201

    redevance_actuelle = redevance_communale_des_mines_sel_dissolution_kt[index]
    print("/titre", redevance_actuelle, "€")  # noqa: T201

    for commune in titre_communes:
        print(titre_communes[commune])  # noqa: T201
        nouvelle_redevance_commune = (
            redevance_actuelle * float(titre_communes[commune]) / titre_surface_totale
            )
        print("/commune", commune, nouvelle_redevance_commune)  # noqa: T201
        ligne_resultat = (
            commune,
            redevance_actuelle,
            row.id_x,
            nouvelle_redevance_commune)
        data_reforme.append(ligne_resultat)

resultat = pandas.DataFrame(data_reforme, columns = colonnes)
resultat.to_csv('toto.csv', index=False)
