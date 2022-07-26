import numpy
import pandas  # noqa: I201

from simulations.sip import (
    get_sip_data,
    sip_guyane_cayenne, sip_guyane_cayenne_nom,
    sip_guyane_kourou, sip_guyane_kourou_nom,
    sip_guyane_st_laurent_du_maroni, sip_guyane_st_laurent_du_maroni_nom
    )


def build_designations_entreprises(data):
    nb_lignes = data.shape[0]
    tirets = numpy.full(nb_lignes, ' - ')
    texte_siren = numpy.full(nb_lignes, ' SIREN ')

    return (data["nom_entreprise"] + tirets
        + data["adresse_entreprise"] + tirets
        + data["siren"] + texte_siren)


def calculate_production_communale(data):
    # renseignements_orNet est renseignements_orExtrait à partir des data 2020
    return round(
        data["renseignements_orNet"] * (data["surface_communale"]
        / data["surface_totale"]),
        3)


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
        "Désignation et adresse des concessionnaires,\
            titulaires de permis d’exploitation ou exploitants",
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
        # > renseignements_orExtrait à zéro ; ou renseignements_orNet
        #   (si brut non défini ?)
        # > pour activités.annee en N-1
        # > et activités.period se terminant par 'trimestre'
        #   (1er trimestre, 2e trimestre, 3e trimestre, 4e trimestre)
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
        # > Camino : somme des 4 rapports trimestriels année N-1
        #   (activités.renseignements_environnement)  # noqa: E800
        # > pour activités.annee en N-1 et activités.period en 'année'
        # > = sur l'interface web, activités,
        #   "Dépenses relatives à la protection de l’environnement (euros)"  # noqa: E800, E501
        "Montant net de taxe minière sur l'or de Guyane",
        # -> [col. 15] (col.6 x col.12)-col.14 ou (col.6 x col.13)-col.14
        # ---
        "Frais de gestion de la fiscalité directe locale",
        # -> [col. 16] (col.11 + col.15) x 8%
        "Service de la Direction générale des Finances publiques\
            en charge du recouvrement",
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

    matrice["Numéro d'ordre de la matrice"] = numeros_ordre + 1
    matrice["Commune du lieu principal d'exploitation"] = data[
        "commune_exploitation_principale"
        ]

    matrice[
        "Désignation et adresse des concessionnaires,\
            titulaires de permis d’exploitation ou exploitants"
        ] = build_designations_entreprises(data)

    matrice["Nature des substances extraites"] = numpy.full(
        nb_lignes, 'Minerais aurifères'
        )  # d'après texte législatif
    matrice["Nature"] = numpy.full(
        nb_lignes, "Kilogramme d'or contenu"
        )  # d'après texte législatif

    production_communale = calculate_production_communale(data)
    matrice["Quantités (kg)"] = (production_communale.astype(str))

    # Redevance départementale :
    matrice["Tarifs (RDM)"] = data["tarifs_rdm"]
    matrice["Montant net (RDM)"] = data[
        "redevance_departementale_des_mines_aurifere"
        ]

    # Redevance communale :
    matrice["Tarifs (RCM)"] = data["tarifs_rcm"]
    matrice["Montant net redevance des mines (RCM)"] = data[
        "redevance_communale_des_mines_aurifere"
        ]

    matrice["Total redevance des mines"] = round(
        matrice["Montant net (RDM)"] + matrice["Montant net redevance des mines (RCM)"],
        2)  # TODO vérifier pourquoi la somme a 4 décimales en l'absence d'arrondi

    # Taxe minière sur l'or de Guyane :
    matrice["PME"] = data["taxe_tarif_pme"]
    matrice["Autres entreprises"] = data["taxe_tarif_autres"]
    matrice["Montant des investissements déduits"] = data["investissement"]

    # TODO add check pour la taxe guyane pour l'ensemble des investissements déduits
    # PME et autres entreprises (non PME)
    matrice["Montant net de taxe minière sur l'or de Guyane"] = data["taxe_guyane"]

    matrice["Frais de gestion de la fiscalité directe locale"] = round(
        (matrice["Total redevance des mines"]
        + matrice["Montant net de taxe minière sur l'or de Guyane"]) * 0.08,
        2)

    matrice["Service de la Direction générale des Finances publiques en charge du recouvrement"] = data["drfip"]  # noqa: E501
    matrice["Numéro de l’article du rôle"] = data["titre_id"]
    matrice["Observations, précisions"] = data["observation"]

    matrice.to_csv(
        f'matrice_drfip_guyane_production_{annee_production}_{timestamp}.csv',
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )


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
        # Départements et communes sur le territoire desquels
        # fonctionnent les exploitations :
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

    matrice_annexe["Numéro d'ordre de la matrice"] = numeros_ordre + 1
    matrice_annexe[
        "Désignation des concessionnaires, exploitants ou explorateurs"
        ] = build_designations_entreprises(data)
    matrice_annexe["Désignation des concessions, permis ou explorations"] = data[
        "titre_id"
        ]
    # Départements et communes sur le territoire desquels
    # fonctionnent les exploitations :
    matrice_annexe["Départements"] = numpy.full(nb_lignes, 'Guyane')
    matrice_annexe["Communes"] = data['communes']
    # Tonnages extraits au cours de l'année précédente :
    matrice_annexe["par commune"] = calculate_production_communale(data)
    matrice_annexe["par département"] = matrice_annexe["par commune"]

    matrice_annexe["Observations"] = numpy.where(
        matrice_annexe["par commune"] > 0,
        "production en kilogramme d'or", "")

    matrice_annexe.to_csv(
        f'matrice_annexe_drfip_guyane_production_{annee_production}_{timestamp}.csv',
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )


def generate_matrice_1403_drfip_guyane(data, annee_production, timestamp):
    colonnes_1403 = [
        "Service de la Direction générale des finances publiques en charge du recouvrement",  # Circonscription  # noqa: E501
        "Redevance départementale",  # Produit net = col. 2
        "Redevance communale",  # Produit net = col. 3
        "Taxe minière sur l'or de Guyane",  # Produit net = col. 4
        "Sommes revenant à Région de Guyane",
        "Sommes revenant à Conservatoire de biodiversité",  # Rien en 2020 ?

        # Sommes revenant à l'État :
        "Frais d'assiette et de recouvrement",  # = col. 7
        "Dégrèvements et non-valeurs",  # col. 8 / Rien en 2020 ?
        "Total des colonnes 7 et 8",  # col. 9
        "Total des colonnes 2, 3 ,4 et 9",
        "Nombre d'articles des rôles"
        ]

    matrice_1403 = pandas.DataFrame(columns = colonnes_1403)

    data_sip_cayenne = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_cayenne)
    data_sip_kourou = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_kourou)
    data_sip_st_laurent_du_maroni = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_st_laurent_du_maroni)

    matrice_1403[
        "Service de la Direction générale des finances publiques en charge du recouvrement"  # noqa: E501
        ] = [
        sip_guyane_cayenne_nom,
        sip_guyane_kourou_nom,
        sip_guyane_st_laurent_du_maroni_nom
        ]

    matrice_1403["Redevance départementale"] = [
        data_sip_cayenne[
            "redevance_departementale_des_mines_aurifere"
            ].sum().astype(int),
        data_sip_kourou[
            "redevance_departementale_des_mines_aurifere"
            ].sum().astype(int),
        data_sip_st_laurent_du_maroni[
            "redevance_departementale_des_mines_aurifere"
            ].sum().astype(int)
        ]

    matrice_1403["Redevance communale"] = [
        data_sip_cayenne["redevance_communale_des_mines_aurifere"].sum().astype(int),
        data_sip_kourou["redevance_communale_des_mines_aurifere"].sum().astype(int),
        data_sip_st_laurent_du_maroni[
            "redevance_communale_des_mines_aurifere"
            ].sum().astype(int)
        ]
    matrice_1403["Taxe minière sur l'or de Guyane"] = [
        data_sip_cayenne["taxe_guyane"].sum().astype(int),
        data_sip_kourou["taxe_guyane"].sum().astype(int),
        data_sip_st_laurent_du_maroni["taxe_guyane"].sum().astype(int)
        ]

    total_rdcm_taxe = (
        matrice_1403["Redevance départementale"]
        + matrice_1403["Redevance communale"]
        + matrice_1403["Taxe minière sur l'or de Guyane"]
        )

    matrice_1403["Sommes revenant à Région de Guyane"] = matrice_1403[
        "Taxe minière sur l'or de Guyane"
        ]
    matrice_1403["Sommes revenant à Conservatoire de biodiversité"] = [None, None, None]
    matrice_1403["Frais d'assiette et de recouvrement"] = (
        total_rdcm_taxe * 0.08
        ).astype(int)  # 4.4% mais à 8% en 2020, perte des centimes
    matrice_1403["Dégrèvements et non-valeurs"] = [None,
        None, None]  # 3.6% mais vide en 2020
    matrice_1403["Total des colonnes 7 et 8"] = matrice_1403[
        "Frais d'assiette et de recouvrement"
        ]
    matrice_1403["Total des colonnes 2, 3 ,4 et 9"] = total_rdcm_taxe + matrice_1403[
        "Total des colonnes 7 et 8"
        ]
    matrice_1403["Nombre d'articles des rôles"] = [
        data_sip_cayenne["nom_entreprise"].nunique(),
        data_sip_kourou["nom_entreprise"].nunique(),
        data_sip_st_laurent_du_maroni["nom_entreprise"].nunique()
        ]

    matrice_1403.to_csv(
        f'matrice_1403_drfip_guyane_production_{annee_production}_{timestamp}.csv',
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )


def generate_matrice_1404_sip(columns_1404, data_sip, sip_name):
    matrice_1404_sip = pandas.DataFrame(columns = columns_1404)

    NB_ROWS_SIP = len(data_sip)

    matrice_1404_sip[
        "Service de la direction générale des finances publiques en charge du recouvrement"  # noqa: E501
        ] = [sip_name] * NB_ROWS_SIP
    matrice_1404_sip["Articles des rôles"] = data_sip["titre_id"].index

    # Avant affectation, on valide le bon alignement des articles
    # à défaut d'index commun aux DataFrame
    exploitants_sip_cayenne = build_designations_entreprises(data_sip)
    assert (matrice_1404_sip["Articles des rôles"].values
            == exploitants_sip_cayenne.index).all()
    matrice_1404_sip["Désignation des exploitants"] = exploitants_sip_cayenne.values

    # DEPARTEMENTS ET COMMUNES
    # sur les territoires desquels fonctionnent les exploitations :
    matrice_1404_sip["Départements"] = ['Guyane'] * NB_ROWS_SIP  # col. 4
    # col. 5
    matrice_1404_sip["Communes"] = data_sip["commune_exploitation_principale"].values

    # ELEMENTS SERVANT DE BASE A LA REPARTITION pour chaque exploitation :
    matrice_1404_sip["Revenus imposables à la TFPB (état 1123, col. 3)"] = [
        None] * NB_ROWS_SIP  # vide en drfip

    # Avant affectation, on valide le bon alignement des articles
    # à défaut d'index commun aux DataFrame
    production_communale = calculate_production_communale(data_sip)
    assert (matrice_1404_sip["Articles des rôles"].values
            == production_communale.index).all()
    matrice_1404_sip["Tonnages extraits :"] = production_communale.values

    # REDEVANCE DÉPARTEMENTALE :
    matrice_1404_sip["Produit net de la redevance (RDM)"] = data_sip[
        "redevance_departementale_des_mines_aurifere"
        ].values
    matrice_1404_sip[
        "Sommes revenant aux départements désignés dans la colonne 4 (a)"
        ] = matrice_1404_sip["Produit net de la redevance (RDM)"]

    # REDEVANCE COMMUNALE :
    # col. 10
    matrice_1404_sip["Produit net de la redevance (RCM)"] = data_sip[
        "redevance_communale_des_mines_aurifere"
        ].values
    # > Répartition
    matrice_1404_sip["1ère fraction (col. 10 x 35%)"] = matrice_1404_sip[
        "Produit net de la redevance (RCM)"
        ] * 0.35
    matrice_1404_sip["2ème fraction (col. 10 x 10%)"] = matrice_1404_sip[
        "Produit net de la redevance (RCM)"
        ] * 0.1
    matrice_1404_sip["3ème fraction (col. 10 x 55%)"] = matrice_1404_sip[
        "Produit net de la redevance (RCM)"
        ] * 0.55
    # > Sommes revenant aux communes désignées dans la colonne 5
    # au titre des 1ère et 2ème fractions
    # col. 14
    matrice_1404_sip["1ère fraction (b)"] = matrice_1404_sip[
        "1ère fraction (col. 10 x 35%)"
        ]
    # col. 15
    matrice_1404_sip["2ème fraction (a)"] = matrice_1404_sip[
        "2ème fraction (col. 10 x 10%)"
        ]
    matrice_1404_sip["Total (col. 14 + col. 15)"] = matrice_1404_sip[
        "1ère fraction (b)"
        ] + matrice_1404_sip["2ème fraction (a)"]

    # TAXE MINIÈRE SUR L'OR DE GUYANE
    matrice_1404_sip["Produit net de la taxe"] = data_sip["taxe_guyane"].values
    # > Répartition
    matrice_1404_sip["Région de Guyane"] = matrice_1404_sip["Produit net de la taxe"]
    matrice_1404_sip["Conservatoire"] = [None] * NB_ROWS_SIP  # vide en 2020
    matrice_1404_sip["Observations"] = [None] * NB_ROWS_SIP

    return matrice_1404_sip


def generate_matrices_1404_drfip_guyane(data, annee_production, timestamp):
    colonnes_1404 = [
        "Service de la direction générale des finances publiques en charge du recouvrement",  # SIP  # noqa: E501
        "Articles des rôles",
        "Désignation des exploitants",

        # DEPARTEMENTS ET COMMUNES
        # sur les territoires desquels fonctionnent les exploitations :
        "Départements",  # col. 4
        "Communes",  # col. 5

        # ELEMENTS SERVANT DE BASE A LA REPARTITION pour chaque exploitation :
        "Revenus imposables à la TFPB (état 1123, col. 3)",  # col. 6 / vide en drfip
        "Tonnages extraits :",  # col. 7

        # REDEVANCE DÉPARTEMENTALE :
        "Produit net de la redevance (RDM)",
        "Sommes revenant aux départements désignés dans la colonne 4 (a)",

        # REDEVANCE COMMUNALE :
        "Produit net de la redevance (RCM)",  # col. 10
        # > Répartition
        "1ère fraction (col. 10 x 35%)",
        "2ème fraction (col. 10 x 10%)",
        "3ème fraction (col. 10 x 55%)",
        # > Sommes revenant aux communes désignées dans la colonne 5
        # au titre des 1ère et 2ème fractions
        "1ère fraction (b)",  # col. 14
        "2ème fraction (a)",  # col. 15
        "Total (col. 14 + col. 15)",

        # TAXE MINIÈRE SUR L'OR DE GUYANE
        "Produit net de la taxe",
        # > Répartition
        "Région de Guyane",
        "Conservatoire",  # vide en 2020
        "Observations"
        ]
    # où :
    # (a) Attributions faites au prorata des tonnages indiqués dans la colonne 7.
    # (b) Attributions faites au prorata des revenus indiqués dans la colonne 6.
    # (c) Le produit net de la taxe sur l'or de Guyane est affecté en totalité
    # à la région de Guyane en l'absence de création du conservatoire
    # (d) Dès que la création du conservatoire sera intervenu le produit de la taxe
    # due par les PME sera réparti à parts égales entre la région Guyane
    # et cet organisme et la taxe due par les autres

    data_sip_cayenne = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_cayenne)
    matrice_1404_sip_cayenne = generate_matrice_1404_sip(
        colonnes_1404, data_sip_cayenne, sip_guyane_cayenne_nom)
    matrice_1404_sip_cayenne.to_csv(
        f'matrice_1404_sip_guyane_cayenne_production_{annee_production}_{timestamp}.csv',  # noqa: E501
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )

    data_sip_kourou = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_kourou)
    matrice_1404_sip_kourou = generate_matrice_1404_sip(
        colonnes_1404, data_sip_kourou, sip_guyane_kourou_nom)
    matrice_1404_sip_kourou.to_csv(
        f'matrice_1404_sip_guyane_kourou_production_{annee_production}_{timestamp}.csv',
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )

    data_sip_st_laurent_du_maroni = get_sip_data(
        data, "commune_exploitation_principale", sip_guyane_st_laurent_du_maroni
        )
    matrice_1404_sip_st_laurent_du_maroni = generate_matrice_1404_sip(
        colonnes_1404, data_sip_st_laurent_du_maroni,
        sip_guyane_st_laurent_du_maroni_nom
        )
    matrice_1404_sip_st_laurent_du_maroni.to_csv(
        f'matrice_1404_sip_guyane_st_laurent_du_maroni_production_{annee_production}_{timestamp}.csv',  # noqa: E501
        index=False,
        sep=';',
        encoding='utf-8',
        decimal=','
        )
