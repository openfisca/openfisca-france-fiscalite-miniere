import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem

from openfisca_france_fiscalite_miniere import entities

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))


class CountryTaxBenefitSystem(TaxBenefitSystem):
    def __init__(self):
        super(CountryTaxBenefitSystem, self).__init__(entities.entities)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))
        self.load_parameters(os.path.join(COUNTRY_DIR, 'parameters'))
