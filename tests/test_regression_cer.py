"""Test de régression : le CER du modèle final ne doit pas dépasser 15 %.

Ce test charge les prédictions sauvegardées dans experiments/ et vérifie
que le seuil de validation du brief est respecté.  Il est skippé tant que
le fichier de résultats n'existe pas (début de projet).
"""

import json
from pathlib import Path

import pytest

from src.evaluation.metrics import corpus_cer

RESULTS_PATH = Path("experiments") / "results_test_set.json"
CER_THRESHOLD = 0.15


@pytest.mark.skipif(not RESULTS_PATH.exists(), reason="Résultats non encore générés")
class TestCERRegression:
    def test_trocr_cer_below_threshold(self):
        """TrOCR : CER corpus ≤ 15 % sur le jeu de test."""
        data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        refs = [d["reference"] for d in data]
        hyps = [d["trocr_hypothesis"] for d in data]
        score = corpus_cer(refs, hyps)
        assert score <= CER_THRESHOLD, f"TrOCR CER = {score:.2%} > seuil {CER_THRESHOLD:.0%}"

    def test_kraken_cer_below_threshold(self):
        """Kraken : CER corpus ≤ 15 % sur le jeu de test."""
        data = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        refs = [d["reference"] for d in data]
        hyps = [d["kraken_hypothesis"] for d in data]
        score = corpus_cer(refs, hyps)
        assert score <= CER_THRESHOLD, f"Kraken CER = {score:.2%} > seuil {CER_THRESHOLD:.0%}"
