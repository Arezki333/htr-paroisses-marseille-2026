"""Tests unitaires pour src/evaluation/metrics.py."""

import pytest

from src.evaluation.metrics import cer, wer, corpus_cer, corpus_wer


class TestCER:
    def test_identical_strings_return_zero(self):
        assert cer("bonjour", "bonjour") == pytest.approx(0.0)

    def test_empty_hypothesis_returns_one(self):
        """Hypothèse vide = toute la référence supprimée → CER = 1.0."""
        pytest.skip("Non implémenté")

    def test_one_substitution(self):
        """Un seul caractère substitué sur 5 → CER = 0.2."""
        pytest.skip("Non implémenté")

    def test_empty_reference_raises(self):
        """Référence vide doit lever ValueError."""
        pytest.skip("Non implémenté")

    def test_cer_above_one_possible(self):
        """CER peut dépasser 1.0 si beaucoup d'insertions."""
        pytest.skip("Non implémenté")


class TestWER:
    def test_identical_strings_return_zero(self):
        assert wer("le chat dort", "le chat dort") == pytest.approx(0.0)

    def test_one_word_wrong(self):
        pytest.skip("Non implémenté")


class TestCorpusCER:
    def test_consistent_with_single_cer(self):
        """corpus_cer sur un seul exemple doit égaler cer()."""
        pytest.skip("Non implémenté")

    def test_mismatched_lengths_raise(self):
        pytest.skip("Non implémenté")
