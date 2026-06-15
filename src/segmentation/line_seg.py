"""Segmentation de lignes de texte dans une région ou une page entière."""

from pathlib import Path


def segment_lines(image, region_bbox: tuple | None = None):
    """Segmente les lignes de texte dans une image ou une région.

    Args:
        image: Image source (numpy array).
        region_bbox: Bounding box de la région (x, y, w, h) ou None pour toute la page.

    Returns:
        Liste de dicts avec clés 'bbox', 'polygon', et 'order' (int).
    """
    raise NotImplementedError


def order_lines(lines: list[dict]) -> list[dict]:
    """Trie les lignes dans l'ordre de lecture (haut-bas, gauche-droite).

    Args:
        lines: Liste de dicts de lignes avec clé 'bbox'.

    Returns:
        Liste triée de dicts de lignes.
    """
    raise NotImplementedError
