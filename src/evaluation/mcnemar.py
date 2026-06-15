"""Test de McNemar pour comparer statistiquement deux modèles HTR."""

from dataclasses import dataclass


@dataclass
class McNemarResult:
    """Résultat du test de McNemar.

    Attributes:
        statistic: Statistique de test chi-carré.
        p_value: p-valeur associée.
        significant: True si p_value < alpha.
        alpha: Seuil de significativité utilisé.
    """

    statistic: float
    p_value: float
    significant: bool
    alpha: float


def mcnemar_test(
    errors_model_a: list[bool],
    errors_model_b: list[bool],
    alpha: float = 0.05,
    continuity_correction: bool = True,
) -> McNemarResult:
    """Applique le test de McNemar pour comparer deux séquences d'erreurs.

    Args:
        errors_model_a: Liste booléenne — True si le modèle A se trompe sur la ligne i.
        errors_model_b: Liste booléenne — True si le modèle B se trompe sur la ligne i.
        alpha: Seuil de significativité.
        continuity_correction: Applique la correction de continuité de Yates.

    Returns:
        McNemarResult avec la statistique, la p-valeur et la décision.

    Raises:
        ValueError: Si les listes n'ont pas la même longueur.
    """
    raise NotImplementedError
