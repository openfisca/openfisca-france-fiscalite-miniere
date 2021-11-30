# Changelog

## 1.2.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir d 01/01/2020.
* Zones impactées : 
  - `variables/redevances.py`
  - `variables/taxes.py`
* Détails :
  - Ajoute les input variables `surface_communale` et `surface_totale`.
  - Ajoute les formules 2020 pour les RDCM aurifères et la taxe sur l'or en Guyane.
    * Proratise les montants de redevances et taxe à la surface d'emprise sur la commune.
  - Cette version représente le code du modèle employé pour la production de matrices fin 2020 (précisément en commit bdcdb7796e4a0f867fbf9ac498edc9b07b7f3c69).

### 1.1.3

* Correction d'un crash et amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : 
  - `openfisca_france_fiscalite_miniere/entities.py`
  - `simulations/*`
* Détails :
  - Correction de CI : ajoute le nom de branche au nom de cache en CI afin de disposer d'un cache par branche.
  - Ajoute la documentation de l'entité `societe`.
  - Regroupe les fichiers de simulation de réforme RCM 2019-2020 dans `simulations/reformes/` et précise la documentation associée.
  - Exclut les fichiers de test de la wheel du modèle.
  - Supprime `.python-version` optionnel et produisant une erreur à la création d'environnement virtuel.

### 1.1.2 [#11](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/11)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : `openfisca_france_fiscalite_miniere/__init__.py`.
* Détails :
  - Corrige le démarrage de l'API Web OpenFisca.
  - Ajoute et documente les commandes d'installation, de test pour le développement et d'exécution de l'API Web.

### 1.1.1 [#9](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/9)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2020.
* Détails :
  - Revalorise la taxe minière sur l'or en Guyane pour 2020.
  - Revalorise les tarifs RCM tous produits pour 2020.
  - Revalorise les tarifs RDM tous produits pour 2020.

## 1.1.0 [#8](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/8)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Détails :
  - Ajoute une entité `Commune`
  - Ajoute la variable `redevance_communale_totale_sel` (tous types de sel)
  - Ajoute dans `simulations/` les réformes de répartition communale de la Redevance Communale des Mines (RCM) pour le sel en dissolution (`test_essai_selh.py`) et le sel par abattage (`test_essai_selg.py`)
    - Réformes évaluées pour la fiscalité du sel au Grand Est en 2019 sur la base de données de déclaration de production de 2018
    - Colonnes des fichiers de données de production de la réforme décrits en `data_activites.csv` et `data_titres.csv` (format d'export de [Camino](https://camino.beta.gouv.fr))


# 1.0.0 [#6](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/6)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Détails :
  - Permet le calcul des redevances du sel.

### 0.1.2 [#4](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/4)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : toutes.
* Détails :
  - Corrige les règles de calcul des taxes et redevances selon les taux et assiettes en vigueur par années d'imposition.

### 0.1.1 [#5](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/5)

* Changement mineur.
* Zones impactées : `README.md`.
* Détails :
  - Ajout de la feuille de route.

## 0.1.0 [#3](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/3)

* Évolution du système socio-fiscal
* Périodes concernées : toutes.
* Zones impactées : `redevances.py`, `taxes.py`.
* Détails :
  - Ajout des redevances départementales et communales des mines.
  - Ajout de la taxe des mines Guyane.
