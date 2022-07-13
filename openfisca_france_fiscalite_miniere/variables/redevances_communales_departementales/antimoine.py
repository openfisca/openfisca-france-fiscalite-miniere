from numpy import ndarray

from . import BaseQuantite, BaseRedevanceCommunale, BaseRedevanceDepartementale


class quantite_antimoine_t(BaseQuantite):
    label = "Quantité extraite de minerai d'antimoine (par tonne d'antimoine contenu)"


class redevance_communale_des_mines_antimoine(BaseRedevanceCommunale):
    label = "Redevance communale des mines pour le minerai d'antimoine"

    def formula_2020_01(articles, period, parameters) -> ndarray:
        return BaseRedevanceCommunale.base_formula_2020_01(articles, period, parameters, "antimoine", "t")


class redevance_departementale_des_mines_antimoine(BaseRedevanceDepartementale):
    label = "Redevance départementale des mines pour le minerai d'antimoine"

    def formula_2020_01(articles, period, parameters) -> ndarray:
        return BaseRedevanceDepartementale.base_formula_2020_01(articles, period, parameters, "antimoine", "t")
