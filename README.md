# OpenFisca France — Fiscalité Minière

Système de fiscalité minière française modélisé avec OpenFisca.

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

## Docker

Vous pouvez aussi utiliser Docker pour démarrer le serveur d'API Web. À l'intérieur du répertoire du dépôt `openfisca-france-fiscalite-miniere`, exécuter les commandes suivantes :
```sh
//Build de l’image localement
docker build --no-cache -t openfisca-france-fiscalite-miniere .

//Lancement de l’image
docker run --rm -p 5000:8000 openfisca-france-fiscalite-miniere
```
L'API Web est alors accessible via le port 5000 de l'hôte (8000 du conteneur).
Elle peut être testée dans un autre terminal. Elle renvoie par exemple un message d'accueil au format JSON en cas de requête `curl http://0.0.0.0:5000`.

### Envoyer une première requête à l'API Web

Un exemple de requête simple est donné dans ce fichier :
`./openfisca_france_fiscalite_miniere/examples/societe.json`

Pour transmettre la requête à l'API Web démarrée, dans un autre terminal, aller dans le répertoire du fichier JSON et envoyer la requête avec les commandes suivantes :

```
cd ./openfisca_france_fiscalite_miniere/examples
curl -X POST http://localhost:5000/calculate -H 'Content-Type: application/json' -d @societe.json
```

## Simulations

Le modèle `openfisca_france_fiscalite_miniere` est employé pour la simulation de réformes et l'estimation des effets de la loi sur la base de données de production minière protégées (non fournies).  
Les scripts de simulation sont assemblés dans le répertoire `./simulations`.  

### Réformes de la RCM

Il s'agit d'estimations des effets de réformes réalisées début 2020 sur la base de données [Camino](https://camino.beta.gouv.fr).

Ce sont des simulations d'une réforme de répartition communale de la Redevance Communale des Mines (RCM) pour les exploitations de chaque type de sel : pour chaque concession (titre) d'une mine, les simulations évaluent la distribution de la production et du produit de la taxe au prorata de la surface du titre sur chaque commune.

Elles sont rassemblées dans le répertoire `./simulations/reformes` :

* `test_essai_selg.py` est dédié au sel par abattage,
* `test_essai_selh.py` est dédié au sel en dissolution.

### Matrices DRFip

La génération de CSV au format des matrices suivantes est exécutable sur la base de données [Camino](https://camino.beta.gouv.fr) (données sécurisées non fournies) :
* REDEVANCE DÉPARTEMENTALE ET COMMUNALE DES MINES TAXE MINIÈRE SUR L'OR DE GUYANE
* ÉTAT ANNEXE À LA MATRICE DES  REDEVANCES, TAXES  ÉTABLIES  POUR  L'ANNÉE

Les données Camino employées en entrée des calculs sont également au format CSV. Leur format est donné dans [simulations/INPUT_DATA.md](./simulations/INPUT_DATA.md)

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
