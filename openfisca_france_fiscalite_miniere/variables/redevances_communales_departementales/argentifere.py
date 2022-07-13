from numpy import ndarray

from . import BaseQuantite, BaseRedevanceCommunale, BaseRedevanceDepartementale


class quantite_argentifere_q(BaseQuantite):
    label = "Quantité extraite de minerai argentifere (par quintal d'argent contenu = par centaine de kilogrammes)"


class redevance_communale_des_mines_argentifere(BaseRedevanceCommunale):
    label = "Redevance communale des mines pour le minerai argentifère"

    def formula_2020_01(articles, period, parameters) -> ndarray:
        return BaseRedevanceCommunale.base_formula_2020_01(articles, period, parameters, "argentifere", "q")


class redevance_departementale_des_mines_argentifere(BaseRedevanceDepartementale):
    label = "Redevance départementale des mines pour le minerai d'argentifère"

    def formula_2020_01(articles, period, parameters) -> ndarray:
        return BaseRedevanceDepartementale.base_formula_2020_01(articles, period, parameters, "argentifere", "q")
