import numpy

from openfisca_core.periods import YEAR
from openfisca_core.variables import Variable

from openfisca_france_fiscalite_miniere import entities


class quantite_aurifere_kg(Variable):
    value_type = float
    entity = entities.Societe
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


class quantite_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Quantité de sel d'abattage (par millier de tonnes)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Quantité de sel raffiné (par millier de tonnes)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class quantite_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Quantité de sel de dissolution (par millier de tonnes de NaCl contenu)"
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006191913/2020-01-01"  # noqa: E501
    definition_period = YEAR


class redevance_communale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance communale des mines pour le minerais aurifères"
    reference = [
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départementale des_mines pour le minerais aurifères"
    reference = [
        "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038686694/2020-01-01",  # noqa: E501
        "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    ]
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.aurifere
        quantites = societes("quantite_aurifere_kg", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_communale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance communale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_abattage
        quantites = societes("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départementale du sel d'abattage"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_abattage
        quantites = societes("quantite_sel_abattage_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_abattage_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départamentale + communale des mines de sel d'abattage"
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
    entity = entities.Societe
    label = "Redevance communale du sel raffiné"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_raffine
        quantites = societes("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départementale du sel raffiné"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_raffine
        quantites = societes("quantite_sel_raffine_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_totale_des_mines_sel_raffine_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départamentale + communale des mines de sel raffiné"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departementale = societes(
            "redevance_departementale_des_mines_sel_raffine_kt",
            period)
        communale = societes(
            "redevance_communale_des_mines_sel_raffine_kt",
            period)
        return departementale + communale


class redevance_communale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance communale du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.communales.sel_dissolution
        quantites = societes("quantite_sel_dissolution_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_departementale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départementale du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006069568/LEGISCTA000006161959/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period, parameters) -> numpy.ndarray:
        annee_production = period.last_year
        taux = parameters(period).redevances.departementales.sel_dissolution
        quantites = societes("quantite_sel_dissolution_kt", annee_production)

        return numpy.round(quantites * taux, decimals = 2)


class redevance_communale_totale_sel(Variable):
    value_type = float
    entity = entities.Commune
    label = "Redevance communale tous types de sels"
    reference = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293413/1987-08-09"  # noqa: E501
    definition_period = YEAR

    def formula(communes, period) -> numpy.ndarray:
        redevance_communale_des_mines_sel_abattage_kt = communes.members(
            "redevance_communale_des_mines_sel_abattage_kt",
            period)
        redevance_communale_des_mines_sel_raffine_kt = communes.members(
            "redevance_communale_des_mines_sel_raffine_kt",
            period)
        redevance_communale_des_mines_sel_dissolution_kt = communes.members(
            "redevance_communale_des_mines_sel_dissolution_kt",
            period)

        return communes.sum(
            redevance_communale_des_mines_sel_abattage_kt
            + redevance_communale_des_mines_sel_raffine_kt
            + redevance_communale_des_mines_sel_dissolution_kt
            )


class redevance_totale_des_mines_sel_dissolution_kt(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départamentale + communale des mines du sel extrait en dissolution par sondage livré en dissolution"  # noqa: E501
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departementale = societes(
            "redevance_departementale_des_mines_sel_dissolution_kt",
            period)
        communale = societes(
            "redevance_communale_des_mines_sel_dissolution_kt",
            period)
        return departementale + communale


class redevance_totale_des_mines_aurifere_kg(Variable):
    value_type = float
    entity = entities.Societe
    label = "Redevance départamentale + communale des mines"
    definition_period = YEAR

    def formula(societes, period) -> numpy.ndarray:
        departementale = societes(
            "redevance_departementale_des_mines_aurifere_kg",
            period)
        communale = societes(
            "redevance_communale_des_mines_aurifere_kg",
            period)
        return departementale + communale
