# OpenFisca France — Fiscalité Minière

Système de fiscalité minière française modélisé avec OpenFisca

## Installation

Ce paquet requiert [Python 3.7](https://www.python.org/downloads/release/python-370/) et [pip](https://pip.pypa.io/en/stable/installing/).

Il est recommandé d'utiliser un [environnement virtuel](https://virtualenv.pypa.io/en/stable/) (_virtualenv_) avec un gestionnaire de _virtualenv_ tel que [Pew](https://github.com/berdario/pew).

### Installation pour le développement

Afin d'installer `OpenFisca-France-Fiscalite-Miniere`, il est nécessaire d'indexer son code et d'installer ses dépendances.

> Si vous disposez d'un environnement virtuel, activez-le à cette étape.

Afin d'installer l'ensemble des librairies nécessaires au développement, dans un terminal, exécuter le commande suivante :

```sh
make install
```

Pour en savoir plus sur cette commande, consulter le tag `install` et ses dépendances dans le fichier `./Makefile`.

### Installation pour la production

```sh
make install-prod
```

## Tester et vérifier une installation

Les tests du module `OpenFisca-France-Fiscalite-Miniere` peuvent être vérifiés par la commande suivante :

```sh
make test
```

Pour en savoir plus sur cette commande, consulter le tag `test` du fichier `./Makefile`.

Le résultat de cette commande doit afficher la ligne suivante :

```sh
...
Success: no issues found in X source files
...
============================== XX passed in X.XXs ==============================
```

🎉 Félicitations, `OpenFisca-France-Fiscalite-Miniere` est prêt à être utilisé !

## Servir l'API Web

Afin d'installer les librairies spécifiques à l'API Web, exécuter cette commande :

```sh
make install-api
```

Puis, démarrer l'API Web avec cette commande :

```sh
make serve
```

Un port par défaut est défini dans le `Makefile` (port `5000`).

Pour en savoir plus sur la commande `openfisca serve` sous-jascente et ses options, consultez la [documentation de référence](https://openfisca.org/doc/openfisca-python-api/openfisca_serve.html).

### Envoyer une première requête à l'API Web

Un exemple de requête simple est donné dans ce fichier :
`./openfisca_france_fiscalite_miniere/examples/societe.json`

Pour transmettre la requête à l'API Web démarrée, dans un autre terminal, aller dans le répertoire du fichier JSON et envoyer la requête avec les commandes suivantes :

```
cd ./openfisca_france_fiscalite_miniere/examples
curl -X POST http://localhost:5000/calculate -H 'Content-Type: application/json' -d @societe.json
```

## Simulations

Les scripts de simulation sont assemblés dans le module `./simulations`.
Ces simulations associent le modèle `openfisca_france_fiscalite_miniere` et des données de production (non fournies).

### Réformes de la RCM

Il s'agit d'estimations des effets de réformes réalisées début 2020 sur la base de données [Camino](https://beta.gouv.fr/startups/camino.html) (données sécurisées non fournies).

Ce sont des simulations d'une réforme de répartition communale de la Redevance Communale
des Mines (RCM) pour les exploitations de chaque type de sel :
pour chaque concession (titre) d'une mine, évaluation de la distribution
de la production et du produit de la taxe au prorata de la surface du titre
sur chaque commune.

Dans `./simulations/reformes` :
* `test_essai_selg.py` est dédié au sel par abattage
* `test_essai_selh.py` est dédié au sel en dissolution

### Matrices DRFip

La génération de CSV au format des matrices suivantes est exécutable sur la base de données [Camino](https://camino.beta.gouv.fr) (données sécurisées non fournies) :
* REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES TAXE MINIÈRE SUR L'OR DE GUYANE
* ÉTAT ANNEXE À LA MATRICE DES  REDEVANCES, TAXES  ÉTABLIES  POUR  L'ANNÉE

#### Export Camino - Titres miniers et autorisations

**id**,nom,type,nature,**domaine**,date_debut,date_fin,date_demande,statut,**substances**,surface_km2,**communes**,forets,**departements**,regions,**administrations_noms**,**titulaires_noms**,**titulaires_adresses**,titulaires_legal,**titulaires_categorie**,**amodiataires_noms**,**amodiataires_adresses**,amodiataires_legal,**amodiataires_categorie**,geojson,reference_ONF,reference_PTMG,reference_DEAL,reference_DEB,reference_RNTM,reference_BRGM,reference_IRSN

#### Export Camino - Activités

> ici 'id' est l'identifiant de l'activité

id,**titre_id**,**type**,statut,**annee**,**periode**,frequence_periode_id,**renseignements_orBrut**,renseignements_orExtrait,renseignements_volumeMinerai,renseignements_mercure,renseignements_carburantDetaxe,renseignements_carburantConventionnel,renseignements_pompes,renseignements_pelles,renseignements_effectifs,renseignements_depensesTotales,**renseignements_environnement**,travaux_1,travaux_2,travaux_3,travaux_4,travaux_5,travaux_6,travaux_7,travaux_8,travaux_9,travaux_10,travaux_11,travaux_12,**complement_texte**,**renseignements_orNet**,indicateursSocialEconomiqueDirect_emploisDirectsTotal,indicateursSocialEconomiqueDirect_etpDirectsTotal,indicateursSocialEconomiqueDirect_emploisDirectsResidents,indicateursSocialEconomiqueDirect_etpDirectsResidents,indicateursSocialEconomiqueDirect_emploisDirectsFr,indicateursSocialEconomiqueDirect_etpDirectsFr,indicateursSocialEconomiqueInirects_emploisIndirectsTotal,indicateursSocialEconomiqueInirects_etpIndirectsTotal,indicateursSocialEconomiqueInirects_emploisIndirectsResidents,indicateursSocialEconomiqueInirects_etpIndirectsResidents,indicateursSocialEconomiqueInirects_emploisIndirectsFr,indicateursSocialEconomiqueInirects_etpIndirectsFr,indicateursConcertationAcceptabilite_reunionPublique,indicateursConcertationAcceptabilite_priseContact,indicateursConcertationAcceptabilite_communicationLocale,complementSocialEconomique_texte,levesTopographiques_typeLevesTopo,levesTopographiques_surfaceLevesTopo,levesTopographiques_complementLevesTopo,cartographieGeologique_surfaceCartographieGeologique,cartographieGeologique_complementCartographie,levesGeochimiques_surfaceLevesGeochimie,levesGeochimiques_lineaireLevesGeochimie,levesGeochimiques_complementLevesGeochimie,levesGeophysiques_surfaceLevesMagnetisme,levesGeophysiques_lineaireLevesMagnetisme,levesGeophysiques_typeLevesMagnetisme,levesGeophysiques_surfaceLevesSpectrometrie,levesGeophysiques_lineaireLevesSpectrometrie,levesGeophysiques_typeLevesSpectrometrie,levesGeophysiques_surfaceLevesPolarisationProvoquee,levesGeophysiques_lineaireLevesPolarisationProvoquee,levesGeophysiques_typeLevesPolarisationProvoquee,levesGeophysiques_surfaceLevesSismiques,levesGeophysiques_lineaireLevesSismiques,levesGeophysiques_typeLevesSismiques,levesGeophysiques_surfaceLevesConductivite,levesGeophysiques_lineaireLevesConductivite,levesGeophysiques_typeLevesConductivite,levesGeophysiques_surfaceLevesAutre,levesGeophysiques_lineaireLevesAutre,levesGeophysiques_typeLevesAutre,levesGeophysiques_complementLevesGeochimie,trancheesPuits_puits,trancheesPuits_lineaireTranchees,trancheesPuits_complementTrancheesPuits,sondages_nombreSondagesTariere,sondages_profondeurMaxSondagesTariere,sondages_profondeurMoySondagesTariere,sondages_lineaireSondagesTarieres,sondages_nombreSondagesDestructifs,sondages_profondeurMaxSondagesDestructifs,sondages_profondeurMoySondagesDestructifs,sondages_lineaireSondagesDestructifss,sondages_nombreSondagesCarottes,sondages_profondeurMaxSondagesCarottes,sondages_profondeurMoySondagesCarottes,sondages_lineaireSondagesCarottes,sondages_complementSondages,Analyses_nombreAnalysesMultiElements,Analyses_listeAnalysesMultiElements,Analyses_listeTraitementMineralurgiques,Analyses_complementAnalyses,etudes_listeEtudes,etudes_complementEtudes,indicateursFinanciersDepensesTotales_depensesTotales,indicateursFinanciersLevesTopographiques_depensesLevesTopographiques,indicateursFinanciersCartographieGeologique_depensesCartographie,indicateursFinanciersLevesGeochimie_depensesLevesGeochimie,indicateursFinanciersLevesGeophysique_depensesLevesGeophysique,indicateursFinanciersLevesTrancheesPuits_depensesLevesTrancheesPuits,indicateursFinanciersSondages_depensesLevesSondagesTarieres,indicateursFinanciersSondages_depensesLevesSondagesDestructifs,indicateursFinanciersSondages_depensesLevesSondagesCarottés,indicateursFinanciersAnalysesMultiElements_depensesAnalysesMultiElements,indicateursFinanciersAnalysesMultiElements_depensesTraitementMineralurgiques,indicateursFinanciersEtudes_depensesEtudeEnvironnementale,indicateursFinanciersEtudes_depensesEtudeEconomiquePreliminaire,indicateursFinanciersEtudes_depensesEtudeEconomiquePreFaisabilite,indicateursFinanciersEtudes_depensesEtudeEconomiqueFaisabilité,indicateursFinanciersEtudes_depensesEtudeSociale,indicateursFinanciersEtudes_depensesEtudessautres,indicateursFinanciersEnvironnement_environnement,indicateursFinanciersCommunication_depensesCommunication,complementFinancier_depensesAutres,complementFinancier_texte,indicateursEnvironnement_carburantDetaxe,indicateursEnvironnement_carburantConventionnel,indicateursEnvironnement_pompes,indicateursEnvironnement_pelles,indicateursEnvironnement_mercure,indicateursEnvironnement_surfaceDeforestee,complementEnvironnement_texte

#### Export Camino - Entreprises

**nom**,**siren**



## Lexique

* RCM = Redevance Communale des Mines
* RDM = Redevance Départementale des Mines
* RDCM = Redevance Départementale et Communale des Mines
* Substances M = Substances non énergétiques (métaux, minéraux)

## Références législatives complémentaires

* [Modalités de la déclaration de production minière à des fins fiscales depuis 1987](https://beta.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293414/1987-08-09)
* Unités prises en compte pour la RCM par produit extrait indiquées dans deux textes :
  - depuis 1987 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006293412/1987-08-09
  - depuis 1991 : https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006294877/2020-03-25
