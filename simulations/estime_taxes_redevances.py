import pandas  # noqa: I201
import time

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100
from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# CONFIGURATION

data_period = 2019
# Camino, export Titres miniers et autorisations :
csv_communes = "/Volumes/Transcend2/beta/camino_2020/20201103-12h35-camino-titres-66.csv"
# Camino, export Activités
csv_titres = "/Volumes/Transcend2/beta/camino_2020/20201103-12h42-camino-activites-53.csv"

# ADAPT INPUT DATA

communes_par_titre : pandas.DataFrame = pandas.read_csv(csv_communes)
production_par_titre : pandas.DataFrame = pandas.read_csv(csv_titres)

filtre_annee_production = production_par_titre['annee'] == data_period
titres_data = production_par_titre[filtre_annee_production]
titres_ids = titres_data.titre_id

# selection des communes des titres pour lesquels nous avons des activités
# 'titre_id' des exports d'activités (csv_titres) = 'id' des exports de titres (csv_communes)
filtre_titres = communes_par_titre['id'].isin(titres_ids.tolist())
communes_data = communes_par_titre[filtre_titres][['id', 'substances', 'communes', 'departements']]
communes_ids = communes_data.communes

# SIMULATION

def build_simulation(period, titres_ids, communes_ids):
  tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()

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
  for k, v in production_par_titre_keys.items():
    simulation.set_input(k, data_period, titres_data[v])
  return simulation


simulation_period = '2020'
simulation = build_simulation(simulation_period, titres_ids, communes_ids)

production_par_titre_keys = {'quantite_aurifere_kg': 'renseignements_orNet'}
simulation = set_simulation_inputs(simulation, production_par_titre_keys)

taxe_guyane_brute = simulation.calculate('taxe_guyane_brute', simulation_period)

# SIMULATION OUTPUT

colonnes = ['titre_id', 'renseignements_orNet', 'taxe_guyane_brute']
estimations = titres_ids

resultat = pandas.DataFrame(estimations, columns = colonnes)

resultat['renseignements_orNet'] = titres_data.renseignements_orNet
resultat['taxe_guyane_brute'] = taxe_guyane_brute

timestamp = time.strftime("%Y%m%d-%H%M%S")
resultat.to_csv(f'estimation_{timestamp}.csv', index=False)
