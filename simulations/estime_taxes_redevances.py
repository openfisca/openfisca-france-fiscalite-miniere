import pandas  # noqa: I201

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100
from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# INPUT DATA

data_period = 2019
csv_titres = "TODO get csv from camino"  # Camino, export Activités
csv_communes = "TODO get csv from camino"  # Camino, export Titres miniers et autorisations

production_par_titre = pandas.read_csv(csv_titres)
communes_par_titre = pandas.read_csv(csv_communes)

filtre_annee_production = production_par_titre['annee'] == data_period
titres_data = production_par_titre[filtre_annee_production]
titres_ids = titres_data.titre_id

# 'titre_id' des exports d'activités (csv_titres) = 'id' des exports de titres (csv_communes)
filtre_titres = communes_par_titre['id'].isin(titres_ids.tolist())
communes_data = communes_par_titre[filtre_titres]
communes_ids = communes_data.communes

# SIMULATION

production_par_titre_keys = {'quantite_aurifere_kg': 'renseignements_orBrut'}  # NaN ?

simulation_period = '2020'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()

simulation_builder = SimulationBuilder()
simulation_builder.create_entities(tax_benefit_system)
simulation_builder.declare_person_entity('societe', titres_ids)

# associer communes et titres
commune_instance = simulation_builder.declare_entity('commune', communes_ids)
titres_des_communes = communes_par_titre.id # un id par titre existant
simulation_builder.join_with_persons(commune_instance, titres_des_communes, None)

simulation = simulation_builder.build(tax_benefit_system)

for k, v in production_par_titre_keys.items():
    simulation.set_input(k, data_period, titres_data[v])

taxe_guyane_brute = simulation.calculate('taxe_guyane_brute', simulation_period)

# SIMULATION OUTPUT

colonnes = ['titre_id', 'renseignements_orBrut', 'taxe_guyane_brute']
estimations = titres_ids

resultat = pandas.DataFrame(estimations, columns = colonnes)

resultat['renseignements_orBrut'] = titres_data.renseignements_orBrut
resultat['taxe_guyane_brute'] = taxe_guyane_brute

resultat.to_csv('estimation.csv', index=False)
