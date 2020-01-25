from openfisca_france_fiscalite_miniere import redevances


def test_nature():
    result = redevances.nature()

    assert(result)


def test_quantite():
    result = redevances.quantite()

    assert(result)
