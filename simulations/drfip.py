import pandas  # noqa: I201
import numpy


def build_designations_entreprises(data):
    nb_lignes = data.shape[0]
    new_lines = numpy.full(nb_lignes, '\n')
    tirets = numpy.full(nb_lignes, ' - ')
    texte_siren = numpy.full(nb_lignes, ' SIREN ')

    return (data["nom_entreprise"] + tirets
        + data["adresse_entreprise"] + tirets
        + data["siren"] + texte_siren)

def calculate_production_communale(data):
    return data["renseignements_orNet"] * (data["surface_communale"] / data["surface_totale"])

def generate_matrice_drfip_guyane(data, annee_production, timestamp):
    '''
    Template MATRICE 1121
    REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES 
    (articles 1519 et 1587 à 1589 du Code général des impôts)
    TAXE MINIÈRE SUR L'OR DE GUYANE
    (article 1599 quinquies B du Code général des impôts)
    '''
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
        "Quantités (kg)",
        # [col. 6]
        # > Camino : OR activités.renseignements_orBrut (cellule potentiellement vide)
        # > renseignements_orExtrait à zéro ; ou renseignements_orNet (si brut non défini ?)
        # > pour activités.annee en N-1 
        # > et activités.period se terminant par 'trimestre' (1er trimestre, 2e trimestre, 3e trimestre, 4e trimestre)
        # Redevance départementale :
        "Tarifs (RDM)",  # [col. 7]
        "Montant net (RDM)",  # [col. 8] (col. 6 x col. 7)
        # Redevance communale :
        "Tarifs (RCM)",  # [col. 9]
        "Montant net redevance des mines (RCM)",  # [col. 10] (col. 6 x col. 9)
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

    matrice = pandas.DataFrame(data, columns = colonnes_1121)

    numeros_ordre = data["titre_id"].index
    nb_lignes = len(numeros_ordre)
    new_lines = numpy.full(nb_lignes, '\n')

    matrice["Numéro d'ordre de la matrice"] = numeros_ordre
    matrice["Commune du lieu principal d'exploitation"] = data["commune_exploitation_principale"]

    matrice[
        "Désignation et adresse des concessionnaires, titulaires de permis d’exploitation ou exploitants"
        ] = build_designations_entreprises(data)

    matrice["Nature des substances extraites"] = numpy.full(nb_lignes, 'Minerais aurifères')  # d'après texte législatif
    matrice["Nature"] = numpy.full(nb_lignes, "Kilogramme d'or contenu")  # d'après texte législatif

    production_communale = calculate_production_communale(data)
    # prefix_proportion_communale = numpy.full(nb_lignes, 'Porportion communale : ')
    matrice["Quantités (kg)"] = (
        # data["renseignements_orNet"].astype(str)
        # + new_lines
        # + prefix_proportion_communale +
        production_communale.astype(str)
        )

    # Redevance départementale :
    matrice["Tarifs (RDM)"] = data["tarifs_rdm"]
    matrice["Montant net (RDM)"] = data["redevance_departementale_des_mines_aurifere_kg"]

    # Redevance communale :
    matrice["Tarifs (RCM)"] = data["tarifs_rcm"]
    matrice["Montant net redevance des mines (RCM)"] = data["redevance_communale_des_mines_aurifere_kg"]
     
    matrice["Total redevance des mines"] = matrice["Montant net (RDM)"] + matrice["Montant net redevance des mines (RCM)"]

    # Taxe minière sur l'or de Guyane :
    matrice["PME"] = data["taxe_tarif_pme"]
    matrice["Autres entreprises"] = data["taxe_tarif_autres"]
    matrice["Montant des investissements déduits"] = data["investissement"]

    # TODO add check
    # pandas.testing.assert_series_equal(data["taxe_guyane_brute"], (
    #     (
    #         (matrice["Quantités (kg)"] * matrice["PME"])
    #             - numpy.where(data["categorie_entreprise"] == "PME", matrice["Montant des investissements déduits"], 0)
    #         ) + (
    #             (matrice["Quantités (kg)"] * matrice["Autres entreprises"])
    #             - numpy.where(data["categorie_entreprise"] != "PME", matrice["Montant des investissements déduits"], 0)
    #             )
    #         ).astype('float32')
    #     )
    matrice["Montant net de taxe minière sur l'or de Guyane"] = data["taxe_guyane_brute"]

    matrice["Frais de gestion de la fiscalité directe locale"] = (
        matrice["Total redevance des mines"] + matrice["Montant net de taxe minière sur l'or de Guyane"]
    ) * 0.08

    matrice["Service de la Direction générale des Finances publiques en charge du recouvrement"] = data["drfip"]
    matrice["Numéro de l’article du rôle"] = data["titre_id"]
    matrice["Observations, précisions"] = data["observation"]

    matrice.to_csv(f'matrice_drfip_guyane_production_{annee_production}_{timestamp}.csv', index=False)


def generate_matrice_annexe_drfip_guyane(data, annee_production, timestamp):
    '''
    Template ÉTAT ANNEXE À LA MATRICE 1122
    REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES 
    TAXE MINIÈRE SUR L'OR DE GUYANE
    ÉTAT ANNEXE À LA MATRICE
    DES  REDEVANCES, TAXES  ÉTABLIES  POUR  L'ANNÉE
    '''

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

    matrice_annexe = pandas.DataFrame(data, columns = colonnes_1122)

    numeros_ordre = data["titre_id"].index
    nb_lignes = len(numeros_ordre)
    new_lines = numpy.full(nb_lignes, '\n')

    matrice_annexe["Numéro d'ordre de la matrice"] = numeros_ordre
    matrice_annexe[
        "Désignation des concessionnaires, exploitants ou explorateurs"
        ] = build_designations_entreprises(data)
    matrice_annexe["Désignation des concessions, permis ou explorations"] = data["titre_id"]
    # Départements et communes sur le territoire desquels fonctionnent les exploitations :
    matrice_annexe["Départements"] = numpy.full(nb_lignes, 'Guyane')
    matrice_annexe["Communes"] = data['communes']
    # Tonnages extraits au cours de l'année précédente :
    matrice_annexe["par commune"] = calculate_production_communale(data)
    production_par_departement = round(matrice_annexe["par commune"].sum(), 2)
    print("!!!!  ", production_par_departement)
    matrice_annexe["par département"] = numpy.full(nb_lignes, production_par_departement)  # total production communale sur chaque ligne

    matrice_annexe["Observations"] = numpy.where(
        matrice_annexe["par commune"] > 0,
        "production en kilogramme d'or", "")

    matrice_annexe.to_csv(f'matrice_annexe_drfip_guyane_production_{annee_production}_{timestamp}.csv', index=False)