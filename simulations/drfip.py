# Template/Matrice 1121
# REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES 
# (articles 1519 et 1587 à 1589 du Code général des impôts)
# TAXE MINIÈRE SUR L'OR DE GUYANE
# (article 1599 quinquies B du Code général des impôts)

colonnes_1121 = [
    "Numéro d'ordre de la matrice",  # [col. 1]
    "Commune du lieu principal d'exploitation",  # [col. 2]
    "Désignation et adresse des concessionnaires, titulaires de permis d’exploitation ou exploitants",
        # [col. 3]
        # (lorsqu’il s’agit d’une mine amodiée, porter à l’encre rouge la désignation
        # et l’adresse de l’exploitant au-dessous de celle du concessionnaire)
    "Nature des substances extraites",  # [col. 4]
    # Base des redevances :
    "Nature",  # [col. 5]
    "Quantités",  # [col. 6]
    # Redevance départementale :
    "Tarifs",  # [col. 7]
    "Montant net",  # [col. 8] (col. 6 x col. 7)
    # Redevance communale :
    "Tarifs",  # [col. 9]
    "Montant net redevance des mines",  # [col. 10] (col. 6 x col. 9)
    # ---
    "Total redevance des mines",  # [col. 11] (col.8 + col. 10)
    # Taxe minière sur l'or de Guyane :
    "PME",  # [col. 12] Tarifs par kg extrait pour les...
    "Autres entreprises",  # [col. 13] Tarifs par kg extrait pour les...
    "Montant des investissements déduits",  # [col. 14]
    "Montant net de taxe minière sur l'or de Guyane", # [col. 15] (col.6 x col.12)-col.14 ou (col.6 x col.13)-col.14
    # ---
    "Frais de gestion de la fiscalité directe locale",  # [col. 16] (col.11 + col.15) x 8%
    "Service de la Direction générale des Finances publiques en charge du recouvrement",  # [col. 17]
    "Numéro de l’article du rôle",  # [col. 18]
    "Observations, précisions"  # [col. 19]
]

# Template/Matrice 1122
# REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES 
# TAXE MINIÈRE SUR L'OR DE GUYANE
# ÉTAT ANNEXE À LA MATRICE
# DES  REDEVANCES, TAXES  ÉTABLIES  POUR  L'ANNÉE

colonnes_1122 = [
    "Numéro d'ordre de la matrice",  # [col. 1]
    "Désignation des concessionnaires, exploitants ou explorateurs",  # [col. 2]
    "Désignation des concessions, permis ou explorations",  # [col. 3]
    # Départements et communes sur le territoire desquels fonctionnent les exploitations :
    "Départements",  # [col. 4]
    "Communes",  # [col. 5]
    # Tonnages extraits au cours de l'année précédente :
    "par département",  # [col. 6]
    "par commune",  # [col. 7]
    "Observations"  # [col. 8]
]
