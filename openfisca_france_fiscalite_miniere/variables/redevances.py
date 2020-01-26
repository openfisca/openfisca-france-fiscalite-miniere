import numpy

from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class quantite(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Kilogrammes extraits, dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class nature(variables.Variable):
    value_type = str
    entity = entities.societe
    label = "Substances dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class redevance_departamentale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des mines"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        return _redevances_des_mines(societes, period, parameters, "departamentale")


class redevance_communale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale des mines"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        return _redevances_des_mines(societes, period, parameters, "communale")


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
    annee_imposable = period.last_year
    redevances = parameters(annee_imposable).redevances[perimetre]
    quantites = societes("quantite", annee_imposable)
    natures = societes("nature", annee_imposable)
    tarifs = tuple(redevances[nature] for nature in natures)
    return numpy.round(quantites * tarifs, decimals = 2)
