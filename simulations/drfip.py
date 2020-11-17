# Template MATRICE 1121
# REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES 
# (articles 1519 et 1587 à 1589 du Code général des impôts)
# TAXE MINIÈRE SUR L'OR DE GUYANE
# (article 1599 quinquies B du Code général des impôts)

colonnes_1121 = [
    "Numéro d'ordre de la matrice",  # [col. 1]
    "Commune du lieu principal d'exploitation",
    # [col. 2]
    # > Camino : commune de plus grande surface dans titres.communes
    # > au format commune_1 (float surface);commune_2 (float surface)
    "Désignation et adresse des concessionnaires, titulaires de permis d’exploitation ou exploitants",
        # [col. 3]
        # (lorsqu’il s’agit d’une mine amodiée, porter à l’encre rouge la désignation
        # et l’adresse de l’exploitant au-dessous de celle du concessionnaire)
        # > Camino : adresse de l'amodiataire ou, à défaut, le titulaire.
        # > titres.amodiataires_noms/titres.amodiataires_adresses 
        # > ou titres.titulaires_noms/titres.titulaires_adresses
        # > désignation en amodiataire/titulaire à mémoriser pour le type d'entreprise
    "Nature des substances extraites",
    # [col. 4]
    # > Camino : titres.domaine
    # Base des redevances :
    "Nature",  # [col. 5]
    # > Camino : titres.substances (séparateur ';')
    "Quantités",
    # [col. 6]
    # > Camino : OR activités.renseignements_orBrut (cellule potentiellement vide)
    # > renseignements_orExtrait à zéro ; ou renseignements_orNet (si brut non défini ?)
    # > pour activités.annee en N-1 
    # > et activités.period se terminant par 'trimestre' (1er trimestre, 2e trimestre, 3e trimestre, 4e trimestre)
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
    # > Camino : titres.amodiataires_categorie ou titres.titulaires_categorie
    "Montant des investissements déduits",
    # [col. 14]
    # > Camino : somme des 4 rapports trimestriels année N-1 (activités.renseignements_environnement)
    # > pour activités.annee en N-1 et activités.period en 'année'
    # > = sur l'interface web, activités, "Dépenses relatives à la protection de l’environnement (euros)"
    "Montant net de taxe minière sur l'or de Guyane", # [col. 15] (col.6 x col.12)-col.14 ou (col.6 x col.13)-col.14
    # ---
    "Frais de gestion de la fiscalité directe locale",  # [col. 16] (col.11 + col.15) x 8%
    "Service de la Direction générale des Finances publiques en charge du recouvrement",
    # [col. 17]
    # > Camino : titre.administrations_noms ?
    "Numéro de l’article du rôle",  # [col. 18]
    "Observations, précisions"
    # [col. 19]
    # > Camino : activités.complement_texte ?
]  # une ligne par titre


# Template ÉTAT ANNEXE À LA MATRICE 1122
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
