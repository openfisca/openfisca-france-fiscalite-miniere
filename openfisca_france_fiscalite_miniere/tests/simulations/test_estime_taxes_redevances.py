import logging

from openfisca_france_fiscalite_miniere import (
    CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem
    )

from pandas import DataFrame, Series

import pytest

from simulations.estime_taxes_redevances import (
    clean_data,
    convertit_grammes_a_kilo,
    get_activites_annee,
    get_simulation_full_data,
    get_titres_annee
    )


ANNEE_ACTIVITES = 2019


@pytest.fixture
def communes_par_titre() -> DataFrame:
    # titre_1 a un amodiataire
    # titre_2 est multi-substances et a un titulaire de categorie inconnue
    # titre_3 est multi-communes
    # titre_4 ne fait que passer parce qu'il est d'une période passée
    communes_par_titre = {
        'id': ['titre_1', 'titre_2', 'titre_3', 'titre_4'],
        'domaine': [
            'minéraux et métaux', 'minéraux et métaux',
            'minéraux et métaux', 'minéraux et métaux'
            ],
        'substances': ['or', 'or', 'or;substances connexes', 'or'],
        'communes': [
            'commune_1 (0.123)', 'commune_1 (0.456)',
            'Cayenne_p1 (42.0);Cayenne_p2 (0.216)',
            'temp (0.01)'
            ],
        'departements': ['Guyane', 'MonDepartement', 'Guyane', 'Guyane'],
        'administrations_noms': [
            "\"Ministère de l'Economie et des Finances\
                & Ministère de la Transition écologique et solidaire\
                ;Ministère de l'Economie, des Finances et de la Relance\
                    ;Direction Générale des Territoires et de la Mer de Guyane\
                        ;Préfecture - Guyane;Mission régionnale\
                        autorité environnementale de Guyane\"",
            "Administration d'à côté",
            "\"Ministère de l'Economie et des Finances\
                & Ministère de la Transition écologique et solidaire\
                ;Ministère de l'Economie, des Finances et de la Relance\
                    ;Direction Générale des Territoires et de la Mer de Guyane\
                        ;Préfecture - Guyane;Mission régionnale\
                            autorité environnementale de Guyane\"",
            "Administration d'à côté aussi",
            ],
        'titulaires_noms': [
            'titulaire_1', 'titulaire_autre',
            'titulaire_autre', 'titulaire_4'],
        'titulaires_adresses': [
            'rue du titulaire_1', 'rue du titulaire_autre',
            'rue du titulaire_autre', 'rue du titulaire_4'],
        'titulaires_categorie': ['GE', '', 'PME', 'ETI'],
        'amodiataires_noms': ['amodiataire_1', '', '', ''],
        'amodiataires_adresses': ['rue amodiataire_1', '', '', ''],
        'amodiataires_categorie': ['ETI', '', '', '']
        }

    return DataFrame(data=communes_par_titre)


@pytest.fixture
def activite_par_titre() -> DataFrame:
    # titre_0 n'existe pas dans communes_par_titre
    # titre_1 a un rapport trimestriel (donc pas d'orNet mais des investissements)
    # titre_4 est sur une autre année
    activite_par_titre = {
        'titre_id': ['titre_4', 'titre_3', 'titre_2', 'titre_1', 'titre_0'],
        'annee': ['2018', '2019', '2019', '2018', '2019'],
        'periode': ['année', 'année', 'année', '1er trimestre', 'année'],
        'type': [
            "rapport annuel de production d'or en Guyane",
            "rapport annuel de production d'or en Guyane",
            "rapport annuel de production d'or en Guyane",
            "rapport trimestriel d'exploitation d'or en Guyane",
            "rapport annuel de production d'or en Guyane"
            ],
        'renseignements_orBrut': ['', '', '', 0, ''],  # valeur fournie au trimestre
        'renseignements_orNet': [4000, 3000, 2000, '', 0],  # valeur fournie à l'année
        'renseignements_environnement': ['', '', '', 100, ''],  # valeur fournie au trimestre  # noqa: E501
        'complement_texte': ['nothing', 'rien', 'nada', 'chayn', 'heuu']
        }

    return DataFrame(data=activite_par_titre)


@pytest.fixture
def activites_data(activite_par_titre) -> DataFrame:
    activites_data = get_activites_annee(activite_par_titre, str(ANNEE_ACTIVITES))
    return activites_data


@pytest.fixture
def titres_data(communes_par_titre, activites_data) -> DataFrame:
    titres_data = get_titres_annee(communes_par_titre, activites_data)
    return titres_data


@pytest.fixture
def tax_benefit_system():
    tax_benefit_system = FranceFiscaliteMiniereTaxBenefitSystem()
    return tax_benefit_system


@pytest.fixture
def simulation_data(titres_data, activites_data):
    data_period = 2019
    full_data = get_simulation_full_data(titres_data, activites_data, data_period)
    data = clean_data(full_data, data_period)
    return data


def test_get_activites_annee(activite_par_titre):
    input_years: Series = activite_par_titre['annee'].value_counts(dropna=False)

    activites_data = get_activites_annee(
        activite_par_titre, str(ANNEE_ACTIVITES)
        )  # act

    assert input_years[str(ANNEE_ACTIVITES)] == len(activites_data)


def test_get_titres_annee(communes_par_titre, activite_par_titre, activites_data):
    input_years: Series = activite_par_titre['annee'].value_counts(dropna=False)

    titres_data = get_titres_annee(communes_par_titre, activites_data)  # act

    # seul écart : titre_0 est à la bonne année mais absent des données de titres
    assert set(activites_data.titre_id).symmetric_difference(set(titres_data.id)) == {
        'titre_0'
        }
    assert input_years[str(ANNEE_ACTIVITES)] - 1 == len(titres_data)


def test_get_simulation_full_data(titres_data, activites_data):
    data_period = 2019

    full_data = get_simulation_full_data(
        titres_data,
        activites_data,
        data_period
        )  # act

    assert not full_data.empty
    assert('id' not in full_data.columns)
    assert((full_data['titre_id'] == ['titre_3', 'titre_2']).all())


def test_convertit_grammes_a_kilo():
    simple_data = {'quantites': [0., 1000, 5000.9]}
    data = DataFrame(data=simple_data)
    logging.debug(data)
    logging.debug(data.divide(1000))

    data = convertit_grammes_a_kilo(data, 'quantites')  # act

    assert (data.quantites == [0., 1., 5.0009]).all()
