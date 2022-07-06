# Changelog

### 3.0.2 [#26](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/26)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : `./variables/taxes.py`
* Détails :
  - Corrige l'erreur d'entité à l'appel de `taxe_guyane_brute` et `taxe_guyane_deduction`

### 3.0.1 [#25](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/25)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : N/A
* Détails :
  - Corrige l'erreur d'exécution de l'API Web (`cannot import name 'escape' from 'jinja2`)
  - Met à jour la dépendance `Flask` via la mise à jour d'`OpenFisca-Core`
  - Met à jour l'ignore des affichages console suite à l'évolution de `flake8-print`

# 3.0.0 [#22](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/22)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : 
  - `entities.py`.
  - `variables/*`
* Détails :
  - Renomme l'entité sociéte en article.
  - Ajoute l'entité titre.
  - Ajoute des caractéristiques de titres.

### 2.0.2 [#21](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/21)

* Changement mineur.
* Périodes concernées : à partir du 01/01/2020.
* Zones impactées : 
  - `simulations/drfip.py`
  - `simulations/estime_taxes_redevances.py`
* Détails :
  - Ajoute la génération des matrices 1403 et 1404 aux scripts de `simulations/`.
  - Matrices au format 2021. Code exécuté sur données de production 2020.

### 2.0.1 [#20](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/20)

* Changement mineur.
* Périodes concernées : à partir du 01/01/2020.
* Zones impactées : 
  - `simulations/drfip.py`
  - `simulations/estime_taxes_redevances.py`
* Détails :
  - Adapte les scripts de production des matrices 1121 et 1122 au nouveau format des des données de production.
    * Adapte à l'évolution du format d'export des données de production de Camino.
    * Permet l'emploi des données de production 2019 au format 2020 et des données de production 2020 au format 2021.

# 2.0.0 [#19](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/19)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2014.
* Zones impactées : 
  - `parameters/taxes/guyane/categories/*`
  - `parameters/fiscalite/frais/*`
  - `variables/fiscalite.py` désormais `variables/frais.py`
* Détails :
  - Corrige les frais de gestions à partir de 2014.
    * le paramètre `fiscalite.frais.taux` est supprimé au bénéfice de `frais.taux_assiette_recouvrement` + `frais.taux_degrevement_non_valeur`.
  - Revalorise les tarifs 2021 de la taxe sur l'or en Guyane.
  - Ajoute des descriptions aux déductions de la taxe et frais de gestion de l'État.

### 1.3.2 [#18](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/18)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2021.
* Zones impactées : 
  - `parameters/redevances/departementales/*`
  - `parameters/redevances/communales/*`
* Détails :
  - Revalorise les tarifs 2021 de la redevance départementale des mines (RDM).
  - Couvre tout l'[article 1587 II](https://www.legifrance.gouv.fr/codes/id/LEGIARTI000043663002/2021-06-12/).

### 1.3.1 [#16](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/16)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2021.
* Zones impactées : `parameters/redevances/communales/*`
* Détails :
  - Revalorise les tarifs 2021 de la redevance communale des mines (RCM) hors gisements en mer.
  - Couvre l'[article 1519 II 1°](https://www.legifrance.gouv.fr/codes/id/LEGIARTI000043663105/2021-06-12/).

## 1.3.0 [#10](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/10)

* Évolution du système socio-fiscal. Ajout d'une fonction complémentaire au modèle.
* Périodes concernées : à partir du 01/01/2020.
* Zones impactées :
  - `variables/redevances.py`
  - `variables/taxes.py`
  - `simulations/*`
* Détails :
  - Corrige les divisions par zéro pour RCM et taxe.
  - Ajoute la génération de matrices DRFip pour la production aurifère en Guyane (configurée par `./config.ini`).

### 1.2.1 [#12](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/12)

* Ajout du support de Docker.

## 1.2.0 [#17](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/17)

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

### 1.1.3 [#15](https://github.com/openfisca/openfisca-france-fiscalite-miniere/pull/15)

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
