from openfisca_france_fiscalite_miniere import entities


def test_societe():
    key = "société"

    result = entities.societe

    assert result.key == key
