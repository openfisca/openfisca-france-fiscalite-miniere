import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class CategorieEnum(indexed_enums.Enum):
    pme = "PME"
    autre = "Autre entreprise"


class categorie(variables.Variable):
    value_type = indexed_enums.Enum
    possible_values = CategorieEnum
    default_value = CategorieEnum.pme
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
        params = parameters(annee_imposable).taxes.guyane
        quantites = societes("quantite", annee_imposable)
        categories = societes("categorie", annee_imposable).decode()
        tarifs = (params.categories[categorie.name] for categorie in categories)
        tarifs = numpy.fromiter(tarifs, dtype = float)
        taxes = quantites * tarifs

        annee_investissement = annee_imposable.last_year
        params = parameters(period).taxes.guyane
        investissements = societes("investissement", annee_investissement)
        taux = params.deductions.taux
        montant = params.deductions.montant
        deductions = numpy.amin([investissements, taxes * taux, montant])

        return numpy.round(taxes - deductions, decimals = 2)
