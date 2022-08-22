from numpy import ndarray, round

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_lithium_li2O_t(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Quantité extraite de minerai de lithium (par tonne de Li2O contenu)"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501


class redevance_communale_des_mines_lithium_li20(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Redevance communale des mines pour le minerai de lithium"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"  # noqa: E501
    ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_lithium_li2O_t", annee_production)

        tarif_rcm = parameters(period).redevances.communales.lithium

        rcm = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(rcm, decimals = 2)


class redevance_departementale_des_mines_lithium_li20(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale des mines pour le minerai de lithium"
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"
    ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_lithium_li2O_t", annee_production)

        tarif_rdm = parameters(period).redevances.departementales.lithium
        rdm = (quantite * tarif_rdm) * surface_communale_proportionnee

        return round(rdm, decimals = 2)
