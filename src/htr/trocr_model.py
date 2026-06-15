"""Interface TrOCR (Microsoft) pour la transcription HTR via fine-tuning PEFT/LoRA."""

from pathlib import Path


def load_trocr(model_name: str = "microsoft/trocr-base-handwritten", adapter_path: Path | None = None):
    """Charge le modèle TrOCR avec un adaptateur LoRA optionnel.

    Args:
        model_name: Identifiant HuggingFace du modèle de base.
        adapter_path: Chemin vers les poids PEFT/LoRA fine-tunés, ou None.

    Returns:
        Tuple (model, processor) prêts à l'inférence.

    Raises:
        OSError: Si adapter_path est fourni mais introuvable.
    """
    raise NotImplementedError


def transcribe_line(image, model, processor, max_new_tokens: int = 128) -> str:
    """Transcrit une image de ligne avec TrOCR.

    Args:
        image: Image de ligne (PIL.Image ou numpy array).
        model: Modèle TrOCR chargé.
        processor: Processeur TrOCR associé.
        max_new_tokens: Nombre maximal de tokens générés.

    Returns:
        Texte transcrit (str).
    """
    raise NotImplementedError


def fine_tune(train_dataset, val_dataset, config: dict, output_dir: Path):
    """Lance le fine-tuning TrOCR avec PEFT/LoRA.

    Args:
        train_dataset: Dataset HuggingFace d'entraînement.
        val_dataset: Dataset HuggingFace de validation.
        config: Dictionnaire de hyperparamètres (lr, epochs, batch_size, etc.).
        output_dir: Dossier de sauvegarde des checkpoints.

    Returns:
        None
    """
    raise NotImplementedError
