"""Amélioration du contraste et binarisation des images de manuscrits."""

import cv2
import numpy as np
from skimage.filters import threshold_otsu, threshold_sauvola


def enhance_contrast(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: tuple[int, int] = (8, 8),
) -> np.ndarray:
    """Améliore le contraste d'une image en niveaux de gris via CLAHE.

    CLAHE (Contrast Limited Adaptive Histogram Equalization) applique une
    égalisation locale en découpant l'image en tuiles, ce qui préserve les
    détails fins des manuscrits sans sur-amplifier le bruit.

    Args:
        image: Image en niveaux de gris (np.ndarray, dtype uint8, shape H×W).
            Si une image couleur est fournie (H×W×3), elle est convertie en
            niveaux de gris avant traitement.
        clip_limit: Seuil de coupure du contraste pour éviter la sur-amplification
            du bruit. Valeur typique : 1.0–4.0. Par défaut 2.0.
        tile_grid_size: Dimensions (lignes, colonnes) de la grille de tuiles CLAHE.
            Des tuiles plus petites accentuent les détails locaux. Par défaut (8, 8).

    Returns:
        Image avec contraste amélioré (np.ndarray, dtype uint8, shape H×W).

    Example:
        >>> import numpy as np
        >>> img = np.random.randint(100, 150, (200, 300), dtype=np.uint8)
        >>> out = enhance_contrast(img)
        >>> out.shape == img.shape and out.dtype == np.uint8
        True
    """
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)


def binarize(image: np.ndarray, method: str = "sauvola") -> np.ndarray:
    """Binarise une image en niveaux de gris.

    Deux méthodes sont disponibles :

    * ``'sauvola'`` (défaut) : seuillage local adaptatif basé sur la moyenne et
      l'écart-type locaux de chaque fenêtre. Robuste aux variations d'éclairage
      fréquentes dans les manuscrits anciens.
    * ``'otsu'`` : seuillage global qui minimise la variance inter-classes.
      Plus rapide mais moins précis sur les images à fond non uniforme.

    Args:
        image: Image en niveaux de gris (np.ndarray, dtype uint8, shape H×W).
        method: Algorithme de binarisation. Valeurs acceptées : ``'sauvola'``
            (par défaut) et ``'otsu'``.

    Returns:
        Image binaire (np.ndarray, dtype uint8, shape H×W) avec les valeurs
        0 (noir, encre) et 255 (blanc, fond).

    Raises:
        ValueError: Si ``method`` n'est ni ``'sauvola'`` ni ``'otsu'``.

    Example:
        >>> import numpy as np
        >>> img = np.random.randint(0, 256, (100, 200), dtype=np.uint8)
        >>> out = binarize(img, method='otsu')
        >>> set(np.unique(out)).issubset({0, 255})
        True
    """
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if method == "sauvola":
        thresh = threshold_sauvola(image, window_size=25, k=0.2)
    elif method == "otsu":
        thresh = threshold_otsu(image)
    else:
        raise ValueError(f"Méthode de binarisation inconnue : '{method}'. "
                         "Valeurs acceptées : 'sauvola', 'otsu'.")

    # Texte noir (encre < seuil), fond blanc
    binary = np.where(image >= thresh, 255, 0).astype(np.uint8)
    return binary


def denoise(image: np.ndarray, strength: int = 5) -> np.ndarray:
    """Réduit le bruit d'une image en niveaux de gris via NL-Means.

    Utilise ``cv2.fastNlMeansDenoising`` (Non-Local Means Denoising), une
    méthode qui préserve les bords et les traits fins de l'écriture tout en
    supprimant le bruit de fond.

    Args:
        image: Image en niveaux de gris (np.ndarray, dtype uint8, shape H×W).
        strength: Force du filtre (paramètre ``h`` de NL-Means). Valeurs
            typiques : 3–10. Plus la valeur est élevée, plus le bruit est
            supprimé, au prix d'un léger flou des traits fins. Par défaut 5.

    Returns:
        Image débruitée (np.ndarray, dtype uint8, shape H×W).

    Example:
        >>> import numpy as np
        >>> img = np.random.randint(200, 256, (100, 200), dtype=np.uint8)
        >>> out = denoise(img, strength=5)
        >>> out.shape == img.shape and out.dtype == np.uint8
        True
    """
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return cv2.fastNlMeansDenoising(
        image,
        h=float(strength),
        templateWindowSize=7,
        searchWindowSize=21,
    )
