"""Pipeline de prétraitement complet d'une image de manuscrit."""

from pathlib import Path


def run_pipeline(image_path: Path, output_dir: Path, config: dict | None = None):
    """Exécute le pipeline complet de prétraitement sur une image.

    Args:
        image_path: Chemin vers l'image source.
        output_dir: Dossier de sortie pour l'image traitée.
        config: Dictionnaire de paramètres optionnels (deskew, binarize, etc.).

    Returns:
        Chemin vers l'image prétraitée (Path).

    Raises:
        FileNotFoundError: Si image_path n'existe pas.
    """
    raise NotImplementedError


def batch_pipeline(image_dir: Path, output_dir: Path, config: dict | None = None):
    """Applique run_pipeline sur un dossier entier d'images.

    Args:
        image_dir: Dossier contenant les images source.
        output_dir: Dossier de sortie.
        config: Paramètres de pipeline partagés.

    Returns:
        Liste des chemins d'images prétraitées.
    """
    raise NotImplementedError
