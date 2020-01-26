import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class CategorieEnum(indexed_enums.Enum):
    pme = "PME"
    autre = "Autre entreprise"


class categorie(variables.Variable):
    value_type = indexed_enums.Enum
    possible_values = CategorieEnum
    default_value = CategorieEnum.pme
    entity = entities.societe
    label = "Catégorie d'entreprises, dont l'imposition est prévue par la loi"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class investissement(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Investissements our la réduction des impacts de l'exploitation de l'or sur l'environnement"  # noqa: E501
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class taxe_guyane_brute(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Taxe perçue pour la région de Guyane, avant déduction des investissements"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_imposable = period.last_year
        params = parameters(annee_imposable).taxes.guyane
        quantites = societes("quantite", annee_imposable)
        categories = societes("categorie", annee_imposable).decode()
        tarifs = (params.categories[categorie.name] for categorie in categories)
        tarifs = numpy.fromiter(tarifs, dtype = float)

        return numpy.round(quantites * tarifs, decimals = 2)


class taxe_guyane_deduction(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Investissements déductibles de la taxe perçue pour la région de Guyane"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_imposable = period.last_year
        annee_investissement = annee_imposable.last_year
        params = parameters(period).taxes.guyane
        investissements = societes("investissement", annee_investissement)
        taxes_brutes = societes("taxe_guyane_brute", period)
        taux = params.deductions.taux
        montant = params.deductions.montant

        return numpy.round(
            numpy.amin([investissements, taxes_brutes * taux, montant]),
            decimals = 2,
            )


class taxe_guyane(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Taxe perçue pour la région de Guyane"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        taxes_brutes = societes("taxe_guyane_brute", period)
        deduction = societes("taxe_guyane_deduction", period)

        return numpy.round(taxes_brutes - deduction, decimals = 2)
