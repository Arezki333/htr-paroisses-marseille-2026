"""Configuration du logger centralisé pour le projet HTR."""

import logging
import sys
from pathlib import Path


def get_logger(name: str, level: int = logging.INFO, log_file: Path | None = None) -> logging.Logger:
    """Retourne un logger configuré avec handler console et fichier optionnel.

    Args:
        name: Nom du logger (typiquement __name__ du module appelant).
        level: Niveau de logging (logging.DEBUG, INFO, WARNING, ERROR).
        log_file: Chemin optionnel vers un fichier de log rotatif.

    Returns:
        Logger configuré (logging.Logger).
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    if log_file is not None:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
