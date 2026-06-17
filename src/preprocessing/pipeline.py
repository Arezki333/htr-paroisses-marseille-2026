"""Pipeline de prétraitement complet d'une image de manuscrit."""

from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

from .deskew import deskew
from .enhance import binarize, denoise, enhance_contrast


def run_pipeline(
    image_path: Path,
    output_dir: Path,
    config: dict | None = None,
) -> Path:
    """Exécute le pipeline complet de prétraitement sur une image.

    Applique dans l'ordre :

    1. Conversion en niveaux de gris.
    2. Débruitage (NL-Means, :func:`~.enhance.denoise`).
    3. Amélioration du contraste (CLAHE, :func:`~.enhance.enhance_contrast`).
    4. Correction de l'inclinaison (:func:`~.deskew.deskew`).
    5. Binarisation Sauvola (:func:`~.enhance.binarize`).

    Chaque étape peut être paramétrée via ``config``. Les clés reconnues sont
    ``denoise``, ``enhance_contrast`` et ``binarize`` ; leur valeur doit être
    un dictionnaire de kwargs passé directement à la fonction correspondante.

    Args:
        image_path: Chemin vers l'image source (JPG, PNG, TIFF…).
        output_dir: Dossier de destination. Créé automatiquement s'il
            n'existe pas.
        config: Paramètres optionnels du pipeline, par exemple::

                {
                    "denoise":          {"strength": 3},
                    "enhance_contrast": {"clip_limit": 3.0},
                    "binarize":         {"method": "otsu"},
                }

    Returns:
        Chemin absolu du fichier image prétraité (Path), sauvegardé dans
        ``output_dir`` sous le même nom que ``image_path``.

    Raises:
        FileNotFoundError: Si ``image_path`` n'existe pas.
        ValueError: Si l'image ne peut pas être décodée par OpenCV.

    Example:
        >>> from pathlib import Path
        >>> # run_pipeline(Path("scan.jpg"), Path("out/"))  # doctest: +SKIP
    """
    image_path = Path(image_path)
    output_dir = Path(output_dir)

    if not image_path.exists():
        raise FileNotFoundError(f"Image introuvable : {image_path}")

    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Impossible de décoder l'image : {image_path}")

    cfg = config or {}

    # 1. Niveaux de gris
    gray: np.ndarray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Débruitage
    gray = denoise(gray, **cfg.get("denoise", {}))

    # 3. Amélioration du contraste (CLAHE)
    gray = enhance_contrast(gray, **cfg.get("enhance_contrast", {}))

    # 4. Correction de l'inclinaison
    gray = deskew(gray)

    # 5. Binarisation Sauvola
    binary: np.ndarray = binarize(gray, **cfg.get("binarize", {}))

    # Sauvegarde
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / image_path.name
    cv2.imwrite(str(dest), binary)

    return dest.resolve()


def batch_pipeline(
    image_dir: Path,
    output_dir: Path,
    config: dict | None = None,
) -> list[Path]:
    """Applique :func:`run_pipeline` sur toutes les images JPG d'un dossier.

    Les fichiers sont traités dans l'ordre alphabétique. Une barre de
    progression ``tqdm`` affiche le nom du fichier en cours.

    Args:
        image_dir: Dossier contenant les images source (seuls les fichiers
            ``*.jpg`` à la racine du dossier sont traités).
        output_dir: Dossier de destination, transmis à :func:`run_pipeline`.
        config: Paramètres de pipeline partagés par toutes les images,
            transmis à :func:`run_pipeline`.

    Returns:
        Liste des chemins absolus des images prétraitées (list[Path]),
        dans le même ordre que les fichiers source.

    Raises:
        FileNotFoundError: Si ``image_dir`` n'existe pas.

    Example:
        >>> from pathlib import Path
        >>> # batch_pipeline(Path("data/raw/GG1"), Path("data/processed/GG1"))
    """
    image_dir = Path(image_dir)
    output_dir = Path(output_dir)

    if not image_dir.exists():
        raise FileNotFoundError(f"Dossier source introuvable : {image_dir}")

    jpgs = sorted(image_dir.glob("*.jpg"))
    results: list[Path] = []

    for img_path in tqdm(jpgs, desc=str(image_dir.name), unit="img"):
        dest = run_pipeline(img_path, output_dir, config)
        results.append(dest)

    return results
