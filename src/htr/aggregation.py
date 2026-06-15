"""Agrégation des transcriptions de lignes en texte de page complet."""


def aggregate_page(lines: list[dict]) -> str:
    """Concatène les transcriptions de lignes en texte de page.

    Args:
        lines: Liste de dicts triés avec clés 'order' et 'transcription'.

    Returns:
        Texte de la page (str), lignes séparées par des retours à la ligne.
    """
    raise NotImplementedError


def aggregate_document(pages: list[str]) -> str:
    """Concatène les textes de pages en document complet.

    Args:
        pages: Liste de textes de pages dans l'ordre.

    Returns:
        Texte du document complet (str).
    """
    raise NotImplementedError


def align_predictions(trocr_lines: list[str], kraken_lines: list[str], strategy: str = "vote") -> list[str]:
    """Fusionne les prédictions TrOCR et Kraken ligne par ligne.

    Args:
        trocr_lines: Transcriptions TrOCR.
        kraken_lines: Transcriptions Kraken.
        strategy: Stratégie de fusion ('vote', 'trocr_primary', 'kraken_primary').

    Returns:
        Liste de transcriptions fusionnées.

    Raises:
        ValueError: Si les listes n'ont pas la même longueur.
    """
    raise NotImplementedError
