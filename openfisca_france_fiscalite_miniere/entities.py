from openfisca_core.entities import build_entity


Societe = build_entity(
    key = "societe",
    plural = "societes",
    label = 'Société',
    is_person = True  # = est entité pivot
    )


Commune = build_entity(
    key = "commune",
    plural = "communes",
    label = 'Commune',
    roles = [
        {
            'key': 'societe',
            'plural': 'societes',
            'label': 'Sociétés'
            }
        ]
    )

entities = [Societe, Commune]
