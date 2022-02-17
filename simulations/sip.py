# SIP = services des impôts des particuliers

from typing import List


sip_guyane_cayenne_nom = "SIP de Cayenne"
sip_guyane_cayenne: List[str] = [
    "Montsinery-Tonnegrande", "Ouanary", "Camopi", "Cayenne",
    "Régina", "Remire-Montjoly", "Roura",
    "Saint-Georges", "Matoury"
    ]

sip_guyane_kourou_nom = "SIP de Kourou"
sip_guyane_kourou: List[str] = ["Kourou", "Macouria",
    "Iracoubo", "Sinnamary", "Saint-Élie"]

sip_guyane_st_laurent_du_maroni_nom = "SIP de Saint-Laurent du Maroni"
sip_guyane_st_laurent_du_maroni: List[str] = [
    "Papaichton", "Apatou", "Awala-Yalimapo",
    "Grand-Santi", "Mana", "Saül", "Maripasoula",
    "Saint-Laurent-du-Maroni"
    ]


def get_sip_data(data, column_name, sip):
    filter = data[column_name].isin(sip)  # noqa: A001
    return data[filter]
