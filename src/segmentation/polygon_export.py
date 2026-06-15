"""Export des polygones de segmentation vers les formats PAGE-XML et ALTO."""

from pathlib import Path


def to_page_xml(lines: list[dict], image_path: Path, output_path: Path):
    """Exporte les lignes segmentées au format PAGE-XML.

    Args:
        lines: Liste de dicts de lignes (avec 'polygon', 'order').
        image_path: Chemin de l'image source (pour les métadonnées XML).
        output_path: Chemin du fichier PAGE-XML de sortie.

    Returns:
        None

    Raises:
        IOError: Si l'écriture du fichier échoue.
    """
    raise NotImplementedError


def to_alto_xml(lines: list[dict], image_path: Path, output_path: Path):
    """Exporte les lignes segmentées au format ALTO XML.

    Args:
        lines: Liste de dicts de lignes.
        image_path: Chemin de l'image source.
        output_path: Chemin du fichier ALTO de sortie.

    Returns:
        None
    """
    raise NotImplementedError


def from_page_xml(xml_path: Path) -> list[dict]:
    """Lit un fichier PAGE-XML et retourne les lignes.

    Args:
        xml_path: Chemin vers le fichier PAGE-XML.

    Returns:
        Liste de dicts de lignes avec 'polygon', 'transcription', 'order'.
    """
    raise NotImplementedError
