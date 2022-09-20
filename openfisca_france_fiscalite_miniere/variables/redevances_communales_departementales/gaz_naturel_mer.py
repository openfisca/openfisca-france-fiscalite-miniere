from numpy import ndarray, round

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_gaz_naturel_mer_100km3(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Quantité extraite de gaz naturel en mer (par 100 000 m3  extraits à 1 bar et 15°C)"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501


class redevance_communale_des_mines_gaz_naturel_mer(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Redevance communale des mines pour le gaz naturel en mer"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"
        ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_gaz_naturel_mer_100km3", annee_production)

        tarif_rcm = parameters(period).redevances.communales.gaz_naturel_mer

        rcm = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(rcm, decimals = 2)


class redevance_departementale_des_mines_gaz_naturel_mer(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale des mines pour le gaz naturel en mer"
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
        ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_gaz_naturel_mer_100km3", annee_production)

        tarif_rdm = parameters(period).redevances.departementales.gaz_naturel_mer
        rdm = (quantite * tarif_rdm) * surface_communale_proportionnee

        return round(rdm, decimals = 2)
