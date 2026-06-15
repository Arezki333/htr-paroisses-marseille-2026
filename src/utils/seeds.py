"""Fixation des graines aléatoires pour la reproductibilité des expériences."""

import random


def fixer_seeds(seed: int = 42) -> None:
    """Fixe toutes les graines aléatoires pour garantir la reproductibilité.

    Affecte Python random, NumPy, PyTorch (CPU et GPU) et CUDA.

    Args:
        seed: Valeur de la graine (default 42).

    Returns:
        None
    """
    random.seed(seed)

    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass
