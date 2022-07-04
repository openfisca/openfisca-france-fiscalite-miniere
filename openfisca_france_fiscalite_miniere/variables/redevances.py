import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class surface_communale(Variable):
    value_type = float
    entity = entities.Article
    label = "Surface du titre sur une commune"
    definition_period = YEAR


class surface_totale(Variable):
    value_type = float
    entity = entities.Article
    label = "Surface totale du titre, toutes communes comprises"
    definition_period = YEAR


class redevance_communale_totale_sel(Variable):
    value_type = float
    entity = entities.Commune
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
