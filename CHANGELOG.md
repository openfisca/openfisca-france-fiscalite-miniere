# Changelog

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
