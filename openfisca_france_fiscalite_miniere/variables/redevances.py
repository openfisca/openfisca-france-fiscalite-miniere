import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class NatureEnum(indexed_enums.Enum):
    aurifere = "Or contenu dans les minerais aurifères"
    uranium = "Uranium contenu dans les minerais d'uranium"
    tungstene = "Oxyde de tungstène (WO3) contenu dans les minerais de tungstène"
    argentifères = "Argent contenu dans les minerais argentifères"
    bauxite = "Bauxite"
    fluorine = "Fluorine"


class nature(variables.Variable):
    value_type = indexed_enums.Enum
    possible_values = NatureEnum
    default_value = NatureEnum.aurifere
    entity = entities.societe
    label = "Substances dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class quantite(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Kilogrammes extraits, dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class redevance_departamentale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des mines"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        return _redevances_des_mines(societes, period, parameters, "departamentales")


class redevance_communale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale des mines"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        return _redevances_des_mines(societes, period, parameters, "communales")


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
    params = parameters(annee_imposable).redevances[perimetre]
    quantites = societes("quantite", annee_imposable)
    natures = societes("nature", annee_imposable).decode()
    tarifs = (params[nature.name] for nature in natures)
    tarifs = numpy.fromiter(tarifs, dtype = float)

    return numpy.round(quantites * tarifs, decimals = 2)
