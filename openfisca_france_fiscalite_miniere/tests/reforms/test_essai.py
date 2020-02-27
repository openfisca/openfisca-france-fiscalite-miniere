import numpy as np
import pandas  # TODO pip install pandas
import re

from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_france_fiscalite_miniere import FranceFiscaliteMiniereTaxBenefitSystem
from openfisca_france_fiscalite_miniere.reforms.essai import reforme_repartition


# path_data_titres = './data_activites.csv'
# path_data_activites = './data_titres.csv'


period = '2020'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()


def separe_commune_surface(commune_surface):
    '''Transforme [('Commune1 ', '0.123')] en { 'Commune1': 0.123 }'''

    match = re.match("(.*)\((.*)\)", commune_surface)
    return { match.group(1).strip(): match.group(2).strip() }


titres = pandas.read_csv(path_data_titres)
# pour un titre, communes et leurs surfaces couvertes
# print(titres.columns)
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
for index, communes_surfaces in titres_multicommunes.iteritems():
    liste_communes_surfaces = communes_surfaces.split(';')
    # print(liste_communes_surfaces)
    dict_communes_surfaces = {}
    for i in liste_communes_surfaces:
        dict_communes_surfaces.update(separe_commune_surface(i))
    titres.communes.at[index] = dict_communes_surfaces
    communes_ids.extend(dict_communes_surfaces.keys())

# Suppression des doublons
communes_ids = np.unique(communes_ids)


activites = pandas.read_csv(path_data_activites)
# productions
# print(activites.columns)
# ['id', 'titre_id', 'type', 'statut', 'annee', 'periode', 'frequence_periode_id', 'renseignements_orNet', 'complement_texte']
print(activites)

# selh = sel en dissolution (en référence à H2O)
# selr = sel raffiné

filtre_selh = activites['renseignements_orNet'] == 'selh'
activites_selh = activites[filtre_selh]
print(activites_selh)

print(activites.loc[activites['renseignements_orNet'].str.startswith('selh', na=False)])


simulation_builder = SimulationBuilder()
# simulation_builder.create_entities(tax_benefit_system)
# simulation_builder.declare_person_entity('societe', titres_ids)
simulation = simulation_builder.build_default_simulation(tax_benefit_system, count=len(titres_ids))


# simulation.set_input('quantite_sel_dissolution_kt', period, activites.renseignements_orNet)


redevance_communale_des_mines_sel_dissolution_kt = simulation.calculate('redevance_communale_des_mines_sel_dissolution_kt', period)
print(redevance_communale_des_mines_sel_dissolution_kt)
