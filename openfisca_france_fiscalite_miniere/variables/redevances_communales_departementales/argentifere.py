from numpy import ndarray, round

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_argentifere_100kg(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Quantitié extraite de minerai argentifere (par quintal d'argent contenu = par centaine de kilogrammes)"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501


class redevance_communale_des_mines_argentifere(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Redevance communale des mines pour le minerai argentifère"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"
        ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        tarif_rcm = parameters(period).redevances.communales.argentifere

        annee_production = period.last_year
        quantite = articles("quantite_argentifere_100kg", annee_production)
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        rcm = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(rcm, decimals = 2)


class redevance_departementale_des_mines_argentifere(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale des mines pour le minerai argentifère"
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"
        ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        tarif_rdm = parameters(period).redevances.departementales.argentifere

        annee_production = period.last_year
        quantite = articles("quantite_argentifere_100kg", annee_production)
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        rdm = (quantite * tarif_rdm) * surface_communale_proportionnee
        return round(rdm, decimals = 2)
