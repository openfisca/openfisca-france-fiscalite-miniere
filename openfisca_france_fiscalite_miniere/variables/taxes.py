import numpy

from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class categorie(variables.Variable):
    value_type = str
    entity = entities.societe
    label = "Catégorie d'entreprises, dont l'imposition est prévue par la loi"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class investissement(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Investissements our la réduction des impacts de l'exploitation de l'or sur l'environnement"  # noqa: E501
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR


class taxe_guyane(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Taxe perçue pour la région de Guyane"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000020058694/2020-01-01"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_imposable = period.last_year
        taxes = parameters(annee_imposable).taxes.guyane
        quantites = societes("quantite", annee_imposable)
        categories = societes("categorie", annee_imposable)
        tarifs = tuple(taxes[categorie] for categorie in categories)
        taxes = quantites * tarifs

        annee_investissement = annee_imposable.last_year
        investissements = societes("investissement", annee_investissement)
        deduction = numpy.minimum(investissements, taxes * 0.45)
        deduction = numpy.minimum(deduction, 5000.0)

        return numpy.round(taxes - deduction, decimals = 2)
