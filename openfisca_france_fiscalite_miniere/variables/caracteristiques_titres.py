from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class commune_principale_exploitation(Variable):
    value_type = str
    entity = entities.Titre
    label = "Commune principale du lieu d'exploitation d'un titre"
    definition_period = YEAR


class operateur(Variable):
    value_type = str
    entity = entities.Titre
    label = "Nom de la société opératrice d'un titre"
    definition_period = YEAR
