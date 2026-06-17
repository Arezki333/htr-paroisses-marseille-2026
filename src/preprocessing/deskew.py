"""Correction de l'inclinaison (deskew) des images de manuscrits."""

import cv2
import numpy as np


def estimate_skew_angle(image: np.ndarray) -> float:
    """Estime l'angle d'inclinaison du texte via la transformée de Hough.

    Détecte les bords avec Canny, puis applique HoughLinesP pour trouver
    les segments de droite dominants. L'angle médian des segments dont
    l'inclinaison est comprise entre -45° et +45° est retourné.

    Args:
        image: Image en niveaux de gris (np.ndarray, dtype uint8, shape H×W).
            L'image doit contenir du texte ou des lignes horizontales.

    Returns:
        Angle d'inclinaison estimé en degrés (float), dans l'intervalle
        [-45.0, +45.0]. Retourne 0.0 si aucune ligne exploitable n'est
        détectée.

    Example:
        >>> import numpy as np
        >>> img = np.ones((100, 200), dtype=np.uint8) * 255
        >>> angle = estimate_skew_angle(img)
        >>> isinstance(angle, float)
        True
    """
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Détection de contours (seuils adaptés aux manuscrits anciens)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

    # Transformée de Hough probabiliste
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=80,
        minLineLength=50,
        maxLineGap=10,
    )

    if lines is None:
        return 0.0

    angles: list[float] = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0:
            continue
        angle_deg = np.degrees(np.arctan2(dy, dx))
        # On ne conserve que les lignes quasi-horizontales (-45° à +45°)
        if -45.0 <= angle_deg <= 45.0:
            angles.append(angle_deg)

    if not angles:
        return 0.0

    return float(np.median(angles))


def deskew(image: np.ndarray) -> np.ndarray:
    """Corrige l'inclinaison d'une image en appliquant une rotation inverse.

    Estime l'angle d'inclinaison via :func:`estimate_skew_angle`, puis fait
    pivoter l'image d'un angle opposé. Les bords apparus après rotation sont
    remplis en blanc (255) pour ne pas perturber les étapes suivantes du
    pipeline.

    Args:
        image: Image source en niveaux de gris (np.ndarray, dtype uint8,
            shape H×W). Les images en couleur sont acceptées (H×W×C) mais
            les bords seront remplis de noir sur les canaux non-gris.

    Returns:
        Image redressée (np.ndarray, même dtype et shape que l'entrée).
        Si l'angle estimé est inférieur à 0.1°, l'image originale est
        retournée sans copie.

    Example:
        >>> import numpy as np
        >>> img = np.ones((100, 200), dtype=np.uint8) * 200
        >>> out = deskew(img)
        >>> out.shape == img.shape
        True
    """
    gray = image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = estimate_skew_angle(gray)

    # En dessous de 0.1° la rotation est invisible et coûteuse inutilement
    if abs(angle) < 0.1:
        return image

    h, w = image.shape[:2]
    center = (w / 2.0, h / 2.0)

    # Matrice de rotation inverse (on annule l'angle mesuré)
    M = cv2.getRotationMatrix2D(center, angle=-angle, scale=1.0)

    # borderValue=255 → bords blancs (fond de page)
    rotated = cv2.warpAffine(
        image,
        M,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )
    return rotated
