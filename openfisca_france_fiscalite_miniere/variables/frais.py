import numpy

from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class fiscalite_frais_de_gestion_guyane(variables.Variable):
    value_type = float
    entity = entities.Article
    label = "Frais de gestion de la fiscalité directe locale des mines en Guyane"
    reference = "https://www.collectivites-locales.gouv.fr/files/files/finances_locales/fiscalite_locale/vademecum_fiscalite_directe_locale_collectivites.pdf"  # noqa: E501
    definition_period = periods.YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        redevances = articles("redevance_totale_des_mines_aurifere", period)
        taxes = articles("taxe_guyane", period)

        parametres_frais = parameters(period).frais
        taux = (
            parametres_frais.taux_assiette_recouvrement
            + parametres_frais.taux_degrevement_non_valeur
            )

        return numpy.round((redevances + taxes) * taux, decimals = 2)
