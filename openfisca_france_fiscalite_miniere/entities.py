from openfisca_core.entities import build_entity


Societe = build_entity(
    key = "article",
    plural = "articles",
    label = 'Société',
    is_person = True,  # = est entité pivot
    doc = '''
        Société = titre minier à ce stade.
        Un titre peut aussi être sur plusieurs communes.
        L'une des communes du titre est le lieu principal d'exploitation.
        Il y a une substance extraite par titre.
    '''
    )


Commune = build_entity(
    # suppose qu'il n'y a qu'une commune par société/titre ?
    key = "commune",
    plural = "communes",
    label = 'Commune',
    roles = [
        {
            'key': 'article',
            'plural': 'articles',
            'label': 'Sociétés'
            }
        ]
    )

entities = [Societe, Commune]
