import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class quantite_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Minerais aurifères (par kilogramme d'or contenu)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class redevance_communale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale des_mines pour le minerais aurifères"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des_mines pour le minerais aurifères"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départamentale + communale des mines"
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departamentale = societes(
            "redevance_departementale_des_mines_aurifere_kg",
            period)
        communale = societes(
            "redevance_communale_des_mines_aurifere_kg",
            period)
        return departamentale + communale
