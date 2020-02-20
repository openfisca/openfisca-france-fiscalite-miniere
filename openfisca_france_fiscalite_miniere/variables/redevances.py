import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class quantite_aurifere_kg(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Minerais aurifères (par kilogramme d'or contenu)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"
    definition_period = periods.YEAR


class redevance_departamentale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des mines"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        return _redevances_des_mines(societes, period, parameters, "departamentales")


class redevance_communale_des_mines_aurifere_kg(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale des_mines pour le minerais aurifères"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départamentale + communale des mines"
    definition_period = periods.YEAR

    def formula(societes, period) -> numpy.ndarray:
        departamentale = societes("redevance_departamentale_des_mines", period)
        communale = societes("redevance_communale_des_mines", period)
        return departamentale + communale


def _redevances_des_mines(societes, period, parameters, perimetre) -> numpy.ndarray:
    annee_production = period.last_year
    params = parameters(period).redevances[perimetre]
    quantites = societes("quantite", annee_production)
    natures = societes("nature", period).decode()
    tarifs = (params[nature.name] for nature in natures)
    tarifs = numpy.fromiter(tarifs, dtype = float)

    return numpy.round(quantites * tarifs, decimals = 2)
