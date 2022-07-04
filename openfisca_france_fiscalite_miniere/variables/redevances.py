from numpy import divide, ndarray, zeros

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article, Commune


class surface_communale(Variable):
    value_type = float
    entity = Article
    label = "Surface du titre sur une commune"
    definition_period = YEAR


class surface_totale(Variable):
    value_type = float
    entity = Article
    label = "Surface totale du titre, toutes communes comprises"
    definition_period = YEAR


class surface_communale_proportionnee(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Proportion de la surface communale au regard de la surface totale du titre"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"  # noqa: E501
    ]    

    def formula_2020_01(articles, period) -> ndarray:
        surface_communale = articles("surface_communale", period)
        surface_totale = articles("surface_totale", period)
        surface_nulle = zeros(len(surface_communale))

        return divide(
                surface_communale,
                surface_totale,
                out = surface_nulle,
                where = (surface_totale != 0)
                )


class redevance_communale_totale_sel(Variable):
    value_type = float
    entity = Commune
    label = "Redevance communale tous types de sels"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(communes, period) -> numpy.ndarray:
        redevance_communale_des_mines_sel_abattage_kt = communes.members(
            "redevance_communale_des_mines_sel_abattage_kt",
            period)
        redevance_communale_des_mines_sel_raffine_kt = communes.members(
            "redevance_communale_des_mines_sel_raffine_kt",
            period)
        redevance_communale_des_mines_sel_dissolution_kt = communes.members(
            "redevance_communale_des_mines_sel_dissolution_kt",
            period)

        return communes.sum(
            redevance_communale_des_mines_sel_abattage_kt
            + redevance_communale_des_mines_sel_raffine_kt
            + redevance_communale_des_mines_sel_dissolution_kt
            )
