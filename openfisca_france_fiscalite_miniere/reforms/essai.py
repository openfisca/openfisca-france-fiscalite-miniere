import numpy

from openfisca_core.periods import YEAR
from openfisca_core.reforms import Reform
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class redevance_communale_totale_sel(Variable):
    value_type = float
    entity = entities.Commune
    label = "Redevance communale tous types de sels"
    definition_period = YEAR

    def formula(communes, period):
        return numpy.zeros(2)


class reforme_repartition(Reform):
    name = u'Modification de la repartition'

    def apply(self):
        self.update_variable(redevance_communale_totale_sel)
