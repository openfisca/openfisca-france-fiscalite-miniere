from openfisca_core.entities import build_entity


Article = build_entity(
    key = "article",
    plural = "articles",
    label = 'Article',
    is_person = True,  # = est entité pivot
    doc = '''
        Article = titre minier à ce stade.
        Un titre peut aussi être sur plusieurs communes.
        L'une des communes du titre est le lieu principal d'exploitation.
        Il y a une substance extraite par titre.
    '''
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

entities = [Article, Commune]
