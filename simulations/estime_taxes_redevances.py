import pandas  # noqa: I201

from openfisca_core.simulation_builder import SimulationBuilder  # noqa: I100
from openfisca_france_fiscalite_miniere import CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem  # noqa: E501


# INPUT DATA

data_csv_path = "TODO - path vers csv"
data_period = 2019

production_par_titre = pandas.read_csv(data_csv_path)
filtre_annee_production = production_par_titre['annee'] == data_period

simulation_data = production_par_titre[filtre_annee_production]
print(simulation_data)
titres_ids = simulation_data.titre_id

# SIMULATION

production_par_titre_keys = {'quantite_aurifere_kg': 'renseignements_orBrut'}  # NaN ?

simulation_period = '2020'
tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()

simulation_builder = SimulationBuilder()
simulation_builder.create_entities(tax_benefit_system)
simulation_builder.declare_person_entity('societe', titres_ids)

simulation = simulation_builder.build(tax_benefit_system)

for k, v in production_par_titre_keys.items():
    simulation.set_input(k, data_period, simulation_data[v])
