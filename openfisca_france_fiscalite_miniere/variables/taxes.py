import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class CategorieEnum(indexed_enums.Enum):
    pme = "Petites et Moyennes Entreprises"
    autre = "Autre entreprise"


class categorie(variables.Variable):
    value_type = indexed_enums.Enum
    possible_values = CategorieEnum
    default_value = CategorieEnum.pme
    entity = entities.Societe
    label = "Catégorie d'entreprises, dont l'imposition est prévue par la loi"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class investissement(variables.Variable):
    value_type = float
    entity = entities.Societe
    label = "Investissements pour la réduction des impacts de l'exploitation de l'or sur l'environnement"  # noqa: E501
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class taxe_guyane_brute(variables.Variable):
    value_type = float
    entity = entities.Societe
    label = "Taxe perçue pour la production aurifère en Guyane, avant déduction des investissements"  # noqa: E501
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        quantites = societes("quantite_aurifere_kg", annee_production)
        categories = societes("categorie", annee_production).decode()
        tarifs = (params.categories[categorie.name] for categorie in categories)
        tarifs = numpy.fromiter(tarifs, dtype = float)

        return numpy.round(quantites * tarifs, decimals = 2)


class taxe_guyane_deduction(variables.Variable):
    value_type = float
    entity = entities.Societe
    label = "Investissements déductibles de la taxe perçue pour la région de Guyane"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        investissements = societes("investissement", annee_production)
        taxes_brutes = societes("taxe_guyane_brute", period)
        taux_deduction = params.deductions.taux
        montant_deduction_max = params.deductions.montant

        return numpy.round(
            numpy.minimum(
                montant_deduction_max,
                numpy.minimum(investissements, taxes_brutes * taux_deduction),
                ),
            decimals = 2,
            )


class taxe_guyane(variables.Variable):
    value_type = float
    entity = entities.Societe
    label = "Taxe perçue pour la région de Guyane"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        taxes_brutes = societes("taxe_guyane_brute", period)
        deduction = societes("taxe_guyane_deduction", period)

        return numpy.round(taxes_brutes - deduction, decimals = 2)
