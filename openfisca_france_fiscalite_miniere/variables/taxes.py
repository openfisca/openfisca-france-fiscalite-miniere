import numpy

from openfisca_core import indexed_enums
from openfisca_core.model_api import min_, round_
from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article, Titre


class CategorieEnum(indexed_enums.Enum):
    pme = "Petites et Moyennes Entreprises"
    autre = "Autre entreprise"


class categorie(Variable):
    value_type = indexed_enums.Enum
    possible_values = CategorieEnum
    default_value = CategorieEnum.pme  # ou inconnue pour ne pas calculer la taxe ?
    entity = Titre
    label = "Catégorie d'entreprises, dont l'imposition est prévue par la loi"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031817025/2020-01-01"  # noqa: E501
    definition_period = YEAR


class investissement(Variable):
    value_type = float
    entity = Titre
    label = "Investissements pour la réduction des impacts de l'exploitation de l'or sur l'environnement"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031817025/2020-01-01"  # noqa: E501
    definition_period = YEAR


class taxe_guyane_brute(Variable):
    value_type = float
    entity = Article
    label = "Taxe perçue pour la production aurifère en Guyane, avant déduction des investissements"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031817025/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        quantites = articles("quantite_aurifere_kg", annee_production)
        categories = articles.titre("categorie", annee_production).decode()
        tarifs = (params.categories[categorie.name] for categorie in categories)
        tarifs = numpy.fromiter(tarifs, dtype = float)

        # proratisation à la surface pour l'entité article
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        taxe = (quantites * tarifs) * surface_communale_proportionnee

        return round_(taxe, decimals = 2)

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        quantites = articles("quantite_aurifere_kg", annee_production)
        categories = articles.titre("categorie", annee_production).decode()
        tarifs = (params.categories[categorie.name] for categorie in categories)
        tarifs = numpy.fromiter(tarifs, dtype = float)

        return round_(quantites * tarifs, decimals = 2)


class taxe_guyane_deduction(Variable):
    value_type = float
    entity = Article
    label = "Investissements déductibles de la taxe perçue pour la région de Guyane"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031817025/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        investissements = articles.titre("investissement", annee_production)
        taxes_brutes = articles("taxe_guyane_brute", period)
        taux_deduction = params.deductions.taux
        montant_deduction_max = params.deductions.montant

        # proratisation à la surface pour l'entité article
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        deduction_toutes_communes = round_(
            min_(
                montant_deduction_max,
                min_(investissements, taxes_brutes * taux_deduction),
                ),
            decimals = 2,
            )
        deduction = deduction_toutes_communes * surface_communale_proportionnee

        return round_(deduction, decimals = 2)

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        params = parameters(period).taxes.guyane
        investissements = articles.titre("investissement", annee_production)
        taxes_brutes = articles("taxe_guyane_brute", period)
        taux_deduction = params.deductions.taux
        montant_deduction_max = params.deductions.montant

        return round_(
            min_(
                montant_deduction_max,
                min_(investissements, taxes_brutes * taux_deduction),
                ),
            decimals = 2,
            )


class taxe_guyane(Variable):
    value_type = float
    entity = Article
    label = "Taxe perçue pour la région de Guyane"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031817025/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        taxes_brutes = articles("taxe_guyane_brute", period)
        deduction = articles("taxe_guyane_deduction", period)

        return round_(taxes_brutes - deduction, decimals = 2)
