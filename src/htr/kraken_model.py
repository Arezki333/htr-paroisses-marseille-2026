"""Interface Kraken pour la transcription HTR et le fine-tuning sur manuscrits."""

from pathlib import Path


def load_kraken(model_path: Path):
    """Charge un modèle Kraken depuis un fichier .mlmodel.

    Args:
        model_path: Chemin vers le fichier .mlmodel Kraken.

    Returns:
        Modèle Kraken prêt à l'inférence.

    Raises:
        FileNotFoundError: Si model_path n'existe pas.
    """
    raise NotImplementedError


def transcribe_line(image, model) -> str:
    """Transcrit une image de ligne avec Kraken.

    Args:
        image: Image de ligne (PIL.Image).
        model: Modèle Kraken chargé.

    Returns:
        Texte transcrit (str).
    """
    raise NotImplementedError


def fine_tune(ground_truth_dir: Path, base_model_path: Path, config: dict, output_path: Path):
    """Lance le fine-tuning Kraken (ketos train) sur un corpus annoté.

    Args:
        ground_truth_dir: Dossier contenant les paires image/transcription.
        base_model_path: Modèle de base pour le fine-tuning.
        config: Dictionnaire de paramètres ketos (epochs, lr, device, etc.).
        output_path: Chemin du modèle fine-tuné en sortie.

    Returns:
        None
    """
    raise NotImplementedError
