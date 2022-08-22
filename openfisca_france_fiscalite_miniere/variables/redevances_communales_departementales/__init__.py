from openfisca_core.variables import Variable
from openfisca_france_fiscalite_miniere.entities import Article
from openfisca_core.periods import YEAR
from numpy import ndarray, round


class BaseQuantite(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501


class BaseRedevanceCommunale(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"
    ]

    @staticmethod
    def base_formula_2020_01(articles, period, parameters, matiere, quantite_label) -> ndarray:
        tarif_rcm = parameters(period).redevances.communales[matiere]

        annee_production = period.last_year
        quantite = articles(f'quantite_{matiere}_{quantite_label}', annee_production)
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        rcm = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(rcm, decimals=2)


class BaseRedevanceDepartementale(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"
    ]

    @staticmethod
    def base_formula_2020_01(articles, period, parameters, matiere, quantite_label) -> ndarray:
        tarif_rdm = parameters(period).redevances.departementales[matiere]

        annee_production = period.last_year
        quantite = articles(f'quantite_{matiere}_{quantite_label}', annee_production)
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        rdm = (quantite * tarif_rdm) * surface_communale_proportionnee
        return round(rdm, decimals=2)
