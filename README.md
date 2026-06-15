# HTR Paroisses Marseille 2026

Reconnaissance automatique de texte manuscrit (HTR) sur les registres paroissiaux
et les recensements de population des Archives Municipales de Marseille (XVIe–XIXe s.).

---

## Description

Ce projet compare deux architectures HTR — **TrOCR** (Microsoft, transformeur vision-langage)
et **Kraken** (modèle LSTM récurrent adapté aux manuscrits historiques) — sur un corpus
de documents marseillais numérisés.  L'objectif est d'atteindre un Character Error Rate (CER)
inférieur à **15 %** sur le jeu de test, et de caractériser les biais de représentation
liés à la diversité linguistique (français, occitan, latin, italien) du corpus.

---

## Installation

### Prérequis

- Python ≥ 3.11
- CUDA 11.8+ (optionnel, pour l'entraînement GPU)

### Environnement

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -e ".[dev]"
```

---

## Reproduire les résultats

### 1. Prétraitement

```bash
python -m src.preprocessing.pipeline \
  --input  data/raw/paroissiaux/ \
  --output data/processed/
```

### 2. Segmentation

```bash
python -m src.segmentation.line_seg \
  --input  data/processed/ \
  --output segmentations/
```

### 3. Fine-tuning TrOCR

```bash
python -m src.htr.trocr_model train \
  --config configs/trocr_config.yaml
```

### 4. Fine-tuning Kraken

```bash
python -m src.htr.kraken_model train \
  --config configs/kraken_config.yaml
```

### 5. Évaluation

```bash
python -m src.evaluation.metrics \
  --split data/splits/test.json \
  --output experiments/results_test_set.json
```

### 6. Tests

```bash
pytest tests/ -v
```

---

## Organisation de l'équipe

| Membre | Rôle principal |
|--------|----------------|
| TBD    | Annotation ground truth & eScriptorium |
| TBD    | Prétraitement & segmentation |
| TBD    | Fine-tuning TrOCR |
| TBD    | Fine-tuning Kraken |
| TBD    | Évaluation & rédaction article |

---

## Licence

- **Code** : MIT
- **Données ground truth** : CC BY 4.0 (conformément aux licences HTR-United / CATMuS)
- **Images sources** : domaine public (Archives Municipales de Marseille)
