"""Amélioration du contraste et binarisation des images de manuscrits."""


def binarize(image, method="otsu"):
    """Binarise une image en niveaux de gris.

    Args:
        image: Image source (numpy array).
        method: Algorithme de binarisation ('otsu', 'sauvola', 'niblack').

    Returns:
        Image binaire (numpy array booléen).

    Raises:
        ValueError: Si la méthode n'est pas supportée.
    """
    raise NotImplementedError


def enhance_contrast(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """Améliore le contraste via CLAHE.

    Args:
        image: Image source en niveaux de gris (numpy array).
        clip_limit: Seuil de coupure pour CLAHE.
        tile_grid_size: Taille de la grille de tuiles CLAHE.

    Returns:
        Image avec contraste amélioré (numpy array).
    """
    raise NotImplementedError


def denoise(image, strength=10):
    """Réduit le bruit d'une image.

    Args:
        image: Image source (numpy array).
        strength: Force du débruitage (int).

    Returns:
        Image débruitée (numpy array).
    """
    raise NotImplementedError
