from numpy import ndarray, round

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_sel_abattage_kt(Variable):
    value_type = float
    entity = Article
    label = "Quantité de sel d'abattage (par millier de tonnes)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class redevance_communale_des_mines_sel_abattage(Variable):
    value_type = float
    entity = Article
    label = "Redevance communale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_sel_abattage_kt", annee_production)

        tarif_rcm = parameters(period).redevances.communales.sel_abattage

        rcm = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(rcm, decimals = 2)

    def formula(articles, period, parameters) -> ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_abattage
        quantites = articles("quantite_sel_abattage_kt", annee_production)

        return round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_abattage(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year

        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)
        quantite = articles("quantite_sel_abattage_kt", annee_production)

        tarif_rdm = parameters(period).redevances.departementales.sel_abattage
        rdm = (quantite * tarif_rdm) * surface_communale_proportionnee

        return round(rdm, decimals = 2)

    def formula(articles, period, parameters) -> ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_abattage
        quantites = articles("quantite_sel_abattage_kt", annee_production)

        return round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_abattage(Variable):
    value_type = float
    entity = Article
    label = "Redevance départamentale + communale des mines de sel d'abattage"
    definition_period = YEAR

    def formula(articles, period) -> ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_sel_abattage",
            period)
        communale = articles(
            "redevance_communale_des_mines_sel_abattage",
            period)
        return departementale + communale
