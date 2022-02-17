import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class quantite_aurifere_kg(Variable):
    value_type = float
    entity = entities.Article
    label = "Minerais aurifères (par kilogramme d'or contenu)"
    reference = [
        "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01",
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293412/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501
        ]
    definition_period = YEAR
    documentation = '''
    Pour les minerais aurifères, l'évaluation des tonnages nets des produits
    extraits chaque année et d'après lesquels sera calculée l'année suivante
    la redevance communale des mines a pour base la quantité de métal précieux
    effectivement extraite par le traitement métallurgique.
    '''


class quantite_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Quantité de sel d'abattage (par millier de tonnes)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


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


class redevance_communale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance communale des mines pour le minerais aurifères"
    reference = [
        # répartition
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000030695303/2015-06-06",  # noqa: E501
        # tarification
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR
    documentation = '''
    Dite RCM pour l'or.
    Un arrondi est effectué dans la formule car, par exemple,
    l'article 1519 de 2020 indique :
    "Les tarifs sont arrondis au dizième d'euro le plus proche."
    '''

    def formula_2020_01(articles, period, parameters) -> numpy.ndarray:
        # répartition au prorata de la surface de commune du titre
        # cas appliqué mais règlement inconnu ; à vérifier
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = articles("quantite_aurifere_kg", annee_production)

        surface_communale = articles("surface_communale", annee_production)
        surface_totale = articles("surface_totale", annee_production)

        redevance = numpy.divide(
            (quantites * taux) * surface_communale,
            surface_totale,
            out = numpy.zeros(len(surface_communale)),
            where = (surface_totale != 0)
            )
        return numpy.round(redevance, decimals = 2)

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = articles("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départementale des_mines pour le minerais aurifères"
    reference = [
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        tarif = parameters(period).redevances.departementales.aurifere
        quantites = articles("quantite_aurifere_kg", annee_production)

        # proratisation à la surface pour l'entité article
        # TODO spécifique à la Guyane ?
        surface_communale = articles("surface_communale", annee_production)
        surface_totale = articles("surface_totale", annee_production)

        redevance_nulle = numpy.zeros(len(surface_communale))
        redevance = numpy.divide(
            (quantites * tarif) * surface_communale,
            surface_totale,
            out = redevance_nulle,
            where = (surface_totale != 0)
            )
        return numpy.round(redevance, decimals = 2)

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.aurifere
        quantites = articles("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_communale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance communale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_abattage
        quantites = articles("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départementale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(articles, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_abattage
        quantites = articles("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départamentale + communale des mines de sel d'abattage"
    definition_period = YEAR

    def formula(articles, period) -> numpy.ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_sel_abattage_kt",
            period)
        communale = articles(
            "redevance_communale_des_mines_sel_abattage_kt",
            period)
        return departementale + communale


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


class redevance_totale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Article
    label = "Redevance départamentale + communale des mines"
    definition_period = YEAR

    def formula(articles, period) -> numpy.ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_aurifere_kg",
            period)
        communale = articles(
            "redevance_communale_des_mines_aurifere_kg",
            period)
        return departementale + communale
