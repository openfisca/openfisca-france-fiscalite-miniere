import numpy

from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class fiscalite_frais_de_gestion_guyane(variables.Variable):
    value_type = float
    entity = entities.Societe
    label = "Frais de gestion de la fiscalité directe locale des mines en Guyane"
    reference = "https://www.collectivites-locales.gouv.fr/files/files/finances_locales/fiscalite_locale/vademecum_fiscalite_directe_locale_collectivites.pdf"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        redevances = societes("redevance_totale_des_mines_aurifere_kg", period)
        taxes = societes("taxe_guyane", period)
        taux = parameters(period).fiscalite.frais.taux

        return numpy.round((redevances + taxes) * taux, decimals = 2)
