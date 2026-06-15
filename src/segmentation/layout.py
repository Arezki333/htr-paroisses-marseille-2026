"""Analyse de la mise en page (zones textuelles, colonnes, marges)."""

from pathlib import Path


def detect_regions(image, model_path: Path | None = None):
    """Détecte les régions textuelles dans une image de manuscrit.

    Args:
        image: Image source (numpy array ou PIL.Image).
        model_path: Chemin optionnel vers un modèle de segmentation personnalisé.

    Returns:
        Liste de dicts avec clés 'bbox' (x, y, w, h) et 'type' (str).
    """
    raise NotImplementedError


def classify_region(region_image):
    """Classifie une région en 'text', 'margin', 'decoration', etc.

    Args:
        region_image: Image de la région (numpy array).

    Returns:
        Étiquette de région (str).
    """
    raise NotImplementedError
