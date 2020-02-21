import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class quantite_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Minerais aurifères (par kilogramme d'or contenu)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Quantité de sel d'abattage (par millier de tonnes)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Quantité de sel raffiné (par millier de tonnes)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Quantité de sel de dissolution (par millier de tonnes)"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class redevance_communale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale des mines pour le minerais aurifères"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale des_mines pour le minerais aurifères"
    reference = "https://beta.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_communale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale du sel d'abattage"
    # reference ?
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_abattage
        quantites = societes("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale du sel d'abattage"
    # reference ?
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_abattage
        quantites = societes("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départamentale + communale des mines de sel d'abattage (par millier de tonnes)"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departementale = societes(
            "redevance_departementale_des_mines_sel_abattage_kt",
            period)
        communale = societes(
            "redevance_communale_des_mines_sel_abattage_kt",
            period)
        return departementale + communale


class redevance_communale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance communale du sel raffiné"
    # reference ?
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_raffine
        quantites = societes("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départementale du sel raffiné"
    # reference ?
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_raffine
        quantites = societes("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départamentale + communale des mines de sel raffiné (par millier de tonnes)"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departementale = societes(
            "redevance_departementale_des_mines_sel_raffine_kt",
            period)
        communale = societes(
            "redevance_communale_des_mines_sel_raffine_kt",
            period)
        return departementale + communale


class redevance_totale_des_mines(Variable):
    value_type = float
    entity = entities.societe
    label = "Redevance départamentale + communale des mines"
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departamentale = societes(
            "redevance_departementale_des_mines_aurifere_kg",
            period)
        communale = societes(
            "redevance_communale_des_mines_aurifere_kg",
            period)
        return departamentale + communale
