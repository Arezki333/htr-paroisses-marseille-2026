"""Validation du contrat de données : schéma JSON des splits et des transcriptions."""

import json
from pathlib import Path

SPLIT_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "image_path", "transcription", "source"],
        "properties": {
            "id": {"type": "string"},
            "image_path": {"type": "string"},
            "transcription": {"type": "string"},
            "source": {"type": "string", "enum": ["paroissiaux", "recensements"]},
            "scribe_id": {"type": ["string", "null"]},
            "date": {"type": ["string", "null"]},
        },
    },
}


def validate_split(split_path: Path) -> bool:
    """Valide un fichier de split JSON contre le schéma attendu.

    Args:
        split_path: Chemin vers le fichier JSON (train.json, val.json, test.json).

    Returns:
        True si le fichier est valide.

    Raises:
        jsonschema.ValidationError: Si le schéma n'est pas respecté.
        FileNotFoundError: Si split_path n'existe pas.
    """
    raise NotImplementedError


def validate_all_splits(splits_dir: Path) -> dict[str, bool]:
    """Valide train.json, val.json et test.json dans un dossier.

    Args:
        splits_dir: Dossier contenant les trois fichiers de split.

    Returns:
        Dictionnaire {'train': bool, 'val': bool, 'test': bool}.
    """
    raise NotImplementedError
