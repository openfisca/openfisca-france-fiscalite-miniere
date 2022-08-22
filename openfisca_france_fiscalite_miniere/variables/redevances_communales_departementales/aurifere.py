from numpy import ndarray, round

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_aurifere_kg(Variable):
    value_type = float
    entity = Article
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


class redevance_communale_des_mines_aurifere(Variable):
    value_type = float
    entity = Article
    label = "Redevance communale des mines pour le minerais aurifères"
    reference = [
        # répartition
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000030695303/2015-06-06",
        # tarification
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25",
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR
    documentation = '''
    Dite RCM pour l'or.
    Un arrondi est effectué dans la formule car, par exemple,
    l'article 1519 de 2020 indique :
    "Les tarifs sont arrondis au dizième d'euro le plus proche."
    '''

    def formula_2020_01(articles, period, parameters) -> ndarray:
        # répartition au prorata de la surface de commune du titre
        # mais texte de référence inconnu ;
        # appliqué à la redevance par anticipation de la répartition ?
        annee_production = period.last_year

        tarif_rcm = parameters(period).redevances.communales.aurifere
        quantite = articles("quantite_aurifere_kg", annee_production)
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        redevance = (quantite * tarif_rcm) * surface_communale_proportionnee
        return round(redevance, decimals = 2)

    def formula(articles, period, parameters) -> ndarray:
        annee_production = period.last_year
        tarif = parameters(period).redevances.communales.aurifere
        quantite = articles("quantite_aurifere_kg", annee_production)

        return round(quantite * tarif, decimals = 2)


class redevance_departementale_des_mines_aurifere(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale des mines pour le minerais aurifères"
    reference = [
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01",
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR

    def formula_2020_01(articles, period, parameters) -> ndarray:
        annee_production = period.last_year
        tarif_rdm = parameters(period).redevances.departementales.aurifere
        quantite = articles("quantite_aurifere_kg", annee_production)

        # proratisation à la surface pour l'entité article
        # mais texte de référence inconnu ;
        # appliqué par anticipation de la répartition ?
        surface_communale_proportionnee = articles(
            "surface_communale_proportionnee", annee_production)

        redevance = (quantite * tarif_rdm) * surface_communale_proportionnee
        return round(redevance, decimals = 2)

    def formula(articles, period, parameters) -> ndarray:
        annee_production = period.last_year
        tarif = parameters(period).redevances.departementales.aurifere
        quantite = articles("quantite_aurifere_kg", annee_production)

        return round(quantite * tarif, decimals = 2)


class redevance_totale_des_mines_aurifere(Variable):
    value_type = float
    entity = Article
    label = "Redevance départamentale + communale des mines"
    definition_period = YEAR

    def formula(articles, period) -> ndarray:
        departementale = articles(
            "redevance_departementale_des_mines_aurifere",
            period)
        communale = articles(
            "redevance_communale_des_mines_aurifere",
            period)
        return departementale + communale
