import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities




class quantite_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Quantité de sel raffiné (par millier de tonnes)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Quantité de sel de dissolution (par millier de tonnes de NaCl contenu)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


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


class redevance_communale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance communale du sel raffiné"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_raffine
        quantites = articles("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départementale du sel raffiné"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_raffine
        quantites = articles("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départamentale + communale des mines de sel raffiné"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period) -> numpy.ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_sel_raffine_kt",
            period)
        communale = articles(
            "redevance_communale_des_mines_sel_raffine_kt",
            period)
        return departementale + communale


class redevance_communale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance communale du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_dissolution
        quantites = articles("quantite_sel_dissolution_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départementale du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_dissolution
        quantites = articles("quantite_sel_dissolution_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


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


class redevance_totale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départamentale + communale des mines du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period) -> numpy.ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_sel_dissolution_kt",
            period)
        communale = articles(
            "redevance_communale_des_mines_sel_dissolution_kt",
            period)
        return departementale + communale
