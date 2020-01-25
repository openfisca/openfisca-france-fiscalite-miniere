import numpy

from openfisca_core import indexed_enums
from openfisca_core import periods
from openfisca_core import variables

from openfisca_france_fiscalite_miniere import entities


class Nature(indexed_enums.Enum):
    aurifere = "Or contenu dans des minerais aurifères"


class nature(variables.Variable):
    value_type = indexed_enums.Enum
    default_value = Nature.aurifere
    possible_values = Nature
    entity = entities.societe
    label = "Substances dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class quantite(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Kilogrammes extraits, dont l'imposition est prévue par la loi"
    reference = "https://bofip.impots.gouv.fr/bofip/264-PGP"
    definition_period = periods.YEAR


class redevance_departamentale_des_mines(variables.Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des mines"
    reference = "https://www.legifrance.gouv.fr/affichCode.do;jsessionid=A704355998953570ACB83E8718235B23.tplgfr35s_3?idSectionTA=LEGISCTA000006162672&cidTexte=LEGITEXT000006069577&dateTexte=20200122"  # noqa: E501
    definition_period = periods.YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_imposable = period.last_year()
        quantites = societes("quantite", annee_imposable)
        tarifs = parameters(annee_imposable).redevances.departamentale
        tarif = getattr(tarifs, societes("nature", annee_imposable))

        return quantites * tarif
