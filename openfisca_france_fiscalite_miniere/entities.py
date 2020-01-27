from openfisca_core import entities


class Societe(entities.Entity):
    def __init__(self, key: str, plural: str, label: str, doc: str = "") -> None:
        super().__init__(key, plural, label, doc)


societe = Societe("société", "sociétés", "Société")

entities = [societe]
