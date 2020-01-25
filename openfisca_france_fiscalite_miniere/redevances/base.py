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
