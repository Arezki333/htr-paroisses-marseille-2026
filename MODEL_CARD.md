# Model Card — HTR Paroisses Marseille

## Modèle

| Attribut | TrOCR fine-tuné | Kraken fine-tuné |
|----------|-----------------|------------------|
| Architecture | Vision Encoder-Decoder (ViT + RoBERTa) | LSTM bidirectionnel |
| Modèle de base | `microsoft/trocr-base-handwritten` | CREMMAMedieval / CATMuS |
| Méthode d'adaptation | PEFT / LoRA | Fine-tuning complet (ketos train) |
| Langue cible | Français ancien, occitan, latin | Français ancien, occitan, latin |
| Tâche | Transcription de lignes HTR | Transcription de lignes HTR |

---

## Performances

Résultats sur le jeu de **test** (à compléter après entraînement) :

| Métrique | TrOCR | Kraken | Seuil brief |
|----------|-------|--------|-------------|
| CER corpus | — | — | ≤ 15 % |
| WER corpus | — | — | — |
| mIoU segmentation | — | — | — |
| Test McNemar p-value | — | — | — |

---

## Limitations

- Le modèle est optimisé pour les écritures de scribes provençaux des XVIe–XIXe siècles ;
  ses performances sur d'autres régions ou périodes ne sont pas garanties.
- Les abréviations et ligatures spécifiques au latin notarial peuvent générer des erreurs
  systématiques non capturées par le CER.
- Le corpus d'entraînement est de taille réduite (< 5 000 lignes) ; les performances
  peuvent varier selon le scribe.

---

## Données d'entraînement

| Source | Volume | Langue | Licence |
|--------|--------|--------|---------|
| Archives Municipales de Marseille (GG 1-663) | ~200 pages annotées | Français, latin, occitan | Domaine public |
| HTR-United — CATMuS Medieval | ~10 000 lignes | Latin, français médiéval | CC BY 4.0 |
| HTR-United — CREMMA Medieval | ~8 000 lignes | Français médiéval | CC BY 4.0 |

Voir [DATA_SOURCES.md](DATA_SOURCES.md) pour les détails complets.
