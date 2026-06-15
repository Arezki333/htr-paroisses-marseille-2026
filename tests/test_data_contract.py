"""Tests unitaires pour src/utils/data_contract.py."""

import json
from pathlib import Path

import pytest

from src.utils.data_contract import validate_split, validate_all_splits


VALID_RECORD = {
    "id": "GG001_p001_l001",
    "image_path": "data/processed/GG001_p001_l001.png",
    "transcription": "Baptême de Jean Martin",
    "source": "paroissiaux",
    "scribe_id": None,
    "date": "1693-04-12",
}


class TestValidateSplit:
    def test_valid_split_returns_true(self, tmp_path):
        """Un split conforme au schéma doit être validé sans erreur."""
        pytest.skip("Non implémenté")

    def test_empty_array_is_valid(self, tmp_path):
        """Un split vide [] doit être accepté (pas encore annoté)."""
        pytest.skip("Non implémenté")

    def test_missing_required_field_raises(self, tmp_path):
        """Un enregistrement sans 'transcription' doit lever ValidationError."""
        pytest.skip("Non implémenté")

    def test_invalid_source_enum_raises(self, tmp_path):
        """La valeur 'autre' pour 'source' doit lever ValidationError."""
        pytest.skip("Non implémenté")

    def test_file_not_found_raises(self):
        """validate_split sur un fichier inexistant doit lever FileNotFoundError."""
        pytest.skip("Non implémenté")


class TestValidateAllSplits:
    def test_all_splits_valid(self, tmp_path):
        """validate_all_splits doit retourner True pour les trois splits valides."""
        pytest.skip("Non implémenté")
