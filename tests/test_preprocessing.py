"""Tests unitaires pour le module src/preprocessing."""

import numpy as np
import pytest

from src.preprocessing.deskew import deskew, estimate_skew_angle
from src.preprocessing.enhance import binarize, enhance_contrast, denoise
from src.preprocessing.pipeline import run_pipeline


class TestDeskew:
    def test_deskew_returns_same_shape(self):
        """L'image redressée doit conserver les dimensions originales."""
        pytest.skip("Non implémenté")

    def test_estimate_skew_angle_zero_on_straight_image(self):
        """Une image droite doit retourner un angle proche de 0°."""
        pytest.skip("Non implémenté")

    def test_deskew_raises_on_none(self):
        """deskew doit lever ValueError si l'image est None."""
        pytest.skip("Non implémenté")


class TestEnhance:
    def test_binarize_otsu_returns_binary(self):
        """binarize('otsu') doit retourner une image avec valeurs {0, 255}."""
        pytest.skip("Non implémenté")

    def test_binarize_unsupported_method_raises(self):
        """binarize avec méthode inconnue doit lever ValueError."""
        pytest.skip("Non implémenté")

    def test_enhance_contrast_does_not_change_shape(self):
        """enhance_contrast ne doit pas modifier les dimensions de l'image."""
        pytest.skip("Non implémenté")


class TestPipeline:
    def test_run_pipeline_output_exists(self, tmp_path):
        """run_pipeline doit créer un fichier de sortie dans output_dir."""
        pytest.skip("Non implémenté")

    def test_run_pipeline_raises_on_missing_file(self, tmp_path):
        """run_pipeline doit lever FileNotFoundError si l'image est absente."""
        pytest.skip("Non implémenté")
