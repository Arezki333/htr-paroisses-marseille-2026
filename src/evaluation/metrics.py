"""Métriques d'évaluation HTR : CER, WER, et statistiques de corpus."""


def cer(reference: str, hypothesis: str) -> float:
    """Calcule le Character Error Rate (CER).

    CER = (S + D + I) / N  où S = substitutions, D = suppressions,
    I = insertions, N = nombre de caractères de référence.

    Args:
        reference: Transcription de référence (ground truth).
        hypothesis: Transcription prédite par le modèle.

    Returns:
        CER en proportion [0, ∞) (float).

    Raises:
        ValueError: Si reference est une chaîne vide.
    """
    raise NotImplementedError


def wer(reference: str, hypothesis: str) -> float:
    """Calcule le Word Error Rate (WER).

    Args:
        reference: Transcription de référence.
        hypothesis: Transcription prédite.

    Returns:
        WER en proportion [0, ∞) (float).
    """
    raise NotImplementedError


def corpus_cer(references: list[str], hypotheses: list[str]) -> float:
    """Calcule le CER agrégé sur un corpus entier (somme des éditions / somme des longueurs).

    Args:
        references: Liste des transcriptions de référence.
        hypotheses: Liste des transcriptions prédites.

    Returns:
        CER de corpus (float).

    Raises:
        ValueError: Si les listes n'ont pas la même longueur.
    """
    raise NotImplementedError


def corpus_wer(references: list[str], hypotheses: list[str]) -> float:
    """Calcule le WER agrégé sur un corpus entier.

    Args:
        references: Liste des transcriptions de référence.
        hypotheses: Liste des transcriptions prédites.

    Returns:
        WER de corpus (float).
    """
    raise NotImplementedError
