import pytest
import numpy
from pandas import DataFrame

from openfisca_france_fiscalite_miniere import (
    CountryTaxBenefitSystem as FranceFiscaliteMiniereTaxBenefitSystem
    )
from simulations.estime_taxes_redevances import (
    get_activites_annee,
    get_titres_annee,
    get_simulation_full_data,
    clean_data,
    build_simulation
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
        'domaine': ['minéraux et métaux', 'minéraux et métaux', 'minéraux et métaux', 'minéraux et métaux'],
        'substances': ['or', 'or', 'or;substances connexes', 'or'],
        'communes': ['commune_1 (0.123)', 'commune_1 (0.456)', 'commune_x_p1 (42.0);commune_x_p2 (0.216)', 'temp (0.01)'],
        'departements': ['Guyane', 'MonDepartement', 'Guyane', 'Guyane'],
        'administrations_noms': [
            "\"Ministère de l'Economie et des Finances & Ministère de la Transition écologique et solidaire\
                ;Ministère de l'Economie, des Finances et de la Relance\
                    ;Direction Générale des Territoires et de la Mer de Guyane\
                        ;Préfecture - Guyane;Mission régionnale autorité environnementale de Guyane\"",
            "Administration d'à côté",
            "\"Ministère de l'Economie et des Finances & Ministère de la Transition écologique et solidaire\
                ;Ministère de l'Economie, des Finances et de la Relance\
                    ;Direction Générale des Territoires et de la Mer de Guyane\
                        ;Préfecture - Guyane;Mission régionnale autorité environnementale de Guyane\"",
            "Administration d'à côté aussi",
        ],
        'titulaires_noms': ['titulaire_1', 'titulaire_autre', 'titulaire_autre', 'titulaire_4'],
        'titulaires_adresses': ['rue du titulaire_1', 'rue du titulaire_autre', 'rue du titulaire_autre', 'rue du titulaire_4'],
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
        'renseignements_environnement': ['', '', '', 100, ''],  # valeur fournie au trimestre
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
    full_data = get_simulation_full_data(titres_data, activites_data)
    data = clean_data(full_data)
    return data


def test_get_activites_annee(activite_par_titre):
    activites_data = get_activites_annee(activite_par_titre, str(ANNEE_ACTIVITES))

    input_years: pandas.Series = activite_par_titre['annee'].value_counts(dropna=False)
    assert input_years[str(ANNEE_ACTIVITES)] == len(activites_data)


def test_get_titres_annee(communes_par_titre, activite_par_titre, activites_data):
    titres_data = get_titres_annee(communes_par_titre, activites_data)

    input_years: pandas.Series = activite_par_titre['annee'].value_counts(dropna=False)

    # seul écart : titre_0 est à la bonne année mais absent des données de titres
    assert set(activites_data.titre_id).symmetric_difference(set(titres_data.id)) == { 'titre_0' }
    assert input_years[str(ANNEE_ACTIVITES)]-1 == len(titres_data)


def test_get_simulation_full_data(titres_data, activites_data):
    full_data = get_simulation_full_data(titres_data, activites_data)

    assert not full_data.empty
    assert('id' not in full_data.columns)
    assert((full_data['titre_id'] == ['titre_3', 'titre_2']).all())


def test_clean_data(titres_data, activites_data):
    full_data = get_simulation_full_data(titres_data, activites_data)

    data = clean_data(full_data)

    assert((data['titre_id'] == ['titre_3+commune_x_p1', 'titre_3+commune_x_p2', 'titre_2']).all())


def test_build_simulation(tax_benefit_system, simulation_data):
    simulation = build_simulation(
      tax_benefit_system, ANNEE_ACTIVITES,
      simulation_data.titre_id, simulation_data.communes
      )
    
    simulation_societes = simulation.populations['societe'].ids
    simulation_communes = simulation.populations['commune'].ids

    # ok si pas de doublons sur societes et communes
    unique_societes, unique_societes_counts = numpy.unique(simulation_societes, return_counts=True)
    assert any(count == 1 for count in unique_societes_counts)
    unique_communes, unique_communes_counts = numpy.unique(simulation_communes, return_counts=True)
    assert any(count == 1 for count in unique_communes_counts)
