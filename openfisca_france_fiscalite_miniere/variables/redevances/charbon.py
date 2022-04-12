from numpy import divide, ndarray, round, zeros

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


class quantite_charbon_100t(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Quantité extraite de charbon (par centaine de tonnes nettes extraites)"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25"  # noqa: E501


class redevance_communale_des_mines_charbon(Variable):
    value_type = float
    entity = Article
    definition_period = YEAR
    label = "Redevance communale des mines pour le charbon"
    reference = [
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000042160076/2020-07-25"  # noqa: E501
    ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        def redevance_par_surface(tarif, quantite, surface_article, surface_totale):
            redevance_nulle = zeros(len(surface_article))
            return divide(
                (quantite * tarif) * surface_article,
                surface_totale,
                out = redevance_nulle,
                where = (surface_totale != 0)
                )

        tarif_rcm = parameters(period).redevances.communales.charbon

        annee_production = period.last_year
        quantite = articles("quantite_charbon_100t", annee_production)
        surface_communale = articles("surface_communale", annee_production)
        surface_totale = articles("surface_totale", annee_production)

        rcm = redevance_par_surface(
            tarif_rcm, quantite,
            surface_communale, surface_totale
            )
        return round(rcm, decimals = 2)


class redevance_departementale_des_mines_charbon(Variable):
    value_type = float
    entity = Article
    label = "Redevance départementale des mines pour le charbon"
    definition_period = YEAR
    reference = [
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01",  # noqa: E501
    ]

    def formula_2020_01(articles, period, parameters) -> ndarray:
        def redevance_par_surface(tarif, quantite, surface_article, surface_totale):
            redevance_nulle = zeros(len(surface_article))
            return divide(
                (quantite * tarif) * surface_article,
                surface_totale,
                out = redevance_nulle,
                where = (surface_totale != 0)
                )

        tarif_rdm = parameters(period).redevances.departementales.charbon

        annee_production = period.last_year
        quantite = articles("quantite_charbon_100t", annee_production)
        surface_communale = articles("surface_communale", annee_production)
        surface_totale = articles("surface_totale", annee_production)

        rdm = redevance_par_surface(
            tarif_rdm, quantite,
            surface_communale, surface_totale
            )
        return round(rdm, decimals = 2)
