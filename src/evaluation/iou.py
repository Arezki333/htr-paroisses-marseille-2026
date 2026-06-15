"""Calcul de l'Intersection over Union (IoU) pour évaluer la segmentation."""


def bbox_iou(box_a: tuple, box_b: tuple) -> float:
    """Calcule l'IoU entre deux bounding boxes au format (x, y, w, h).

    Args:
        box_a: Première bounding box (x, y, w, h).
        box_b: Deuxième bounding box (x, y, w, h).

    Returns:
        Score IoU entre 0.0 et 1.0.
    """
    raise NotImplementedError


def polygon_iou(polygon_a: list[tuple], polygon_b: list[tuple]) -> float:
    """Calcule l'IoU entre deux polygones définis par leurs sommets.

    Args:
        polygon_a: Liste de tuples (x, y) définissant le premier polygone.
        polygon_b: Liste de tuples (x, y) définissant le second polygone.

    Returns:
        Score IoU entre 0.0 et 1.0.
    """
    raise NotImplementedError


def mean_iou(ground_truth_lines: list[dict], predicted_lines: list[dict]) -> float:
    """Calcule le mIoU moyen sur un ensemble de lignes segmentées.

    Args:
        ground_truth_lines: Lignes de référence avec clé 'bbox' ou 'polygon'.
        predicted_lines: Lignes prédites avec clé 'bbox' ou 'polygon'.

    Returns:
        mIoU moyen (float).
    """
    raise NotImplementedError
