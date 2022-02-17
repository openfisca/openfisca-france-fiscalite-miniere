from openfisca_core.entities import build_entity


Article = build_entity(
    key = "article",
    plural = "articles",
    label = 'Article',
    is_person = True,  # = est entité pivot
    doc = '''
        Un article est une part d'un unique titre.
        Il est sur une seule commune.
        Il traite d'une seule substance fiscale.
    '''
    )


Titre = build_entity(
    # il n'y a qu'une Titre par article
    key = "titre",
    plural = "titres",
    label = 'Titre',
    roles = [
        {
            'key': 'article',
            'plural': 'articles',
            'label': 'Articles'
            }
        ]
    )


Commune = build_entity(
    # il n'y a qu'une commune par article
    key = "commune",
    plural = "communes",
    label = 'Commune',
    roles = [
        {
            'key': 'article',
            'plural': 'articles',
            'label': 'Articles'
            }
        ]
    )

entities = [Article, Titre, Commune]
