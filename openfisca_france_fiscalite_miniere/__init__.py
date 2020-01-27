import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france_fiscalite_miniere import entities, examples

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        super(CountryTaxBenefitSystem, self).__init__(entities.entities)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))
        self.load_parameters(os.path.join(COUNTRY_DIR, 'parameters'))
        self.open_api_config = {
            "variable_example": "redevance_communale_des_mines",
            "parameter_example": "redevances.communales.aurifere",
            "simulation_example": examples.societe,
            }
