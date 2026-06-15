"""Correction de l'inclinaison (deskew) des images de manuscrits."""


def deskew(image):
    """Corrige l'inclinaison d'une image de manuscrit.

    Args:
        image: Image source (numpy array ou chemin PIL-compatible).

    Returns:
        Image redressée au même format que l'entrée.

    Raises:
        ValueError: Si l'image est None ou vide.
    """
    raise NotImplementedError


def estimate_skew_angle(image):
    """Estime l'angle d'inclinaison d'une image.

    Args:
        image: Image source (numpy array).

    Returns:
        Angle d'inclinaison en degrés (float).
    """
    raise NotImplementedError
