from numpy import divide, ndarray, zeros

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere.entities import Article


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
