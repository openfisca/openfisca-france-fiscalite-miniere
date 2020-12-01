import pytest
from pandas import DataFrame
from simulations.estime_taxes_redevances import get_simulation_full_data, clean_data


@pytest.fixture
def titres_data() -> DataFrame:
    # titre_1 a un amodiataire
    # titre_2 est multi-substances et a un titulaire de categorie inconnue
    # titre_3 est multi-communes
    # titre_4 ne fait que passer parce qu'il est d'une période passée
    titres_data = {
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

    return DataFrame(data=titres_data)


@pytest.fixture
def activites_data() -> DataFrame:
    # titre_0 n'existe pas dans titres_data
    # titre_1 a un rapport trimestriel (donc pas d'orNet mais des investissements)
    # titre_4 est sur une autre année
    activites_data = {
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

    return DataFrame(data=activites_data)


def test_get_simulation_full_data(titres_data, activites_data):
    full_data = get_simulation_full_data(titres_data, activites_data)

    assert('id' not in full_data.columns)
    assert((full_data['titre_id'] == ['titre_3', 'titre_2', 'titre_1']).all())


def test_clean_data(titres_data, activites_data):
    full_data = get_simulation_full_data(titres_data, activites_data)

    data = clean_data(full_data)

    assert((data['titre_id'] == ['titre_3+commune_x_p1', 'titre_3+commune_x_p2', 'titre_2']).all())
