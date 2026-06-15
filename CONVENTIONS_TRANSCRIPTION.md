# Conventions de transcription

Ce document définit les règles d'annotation du ground truth utilisées dans eScriptorium
et exportées vers HTR-United.  Toute l'équipe **doit** les respecter pour garantir la
cohérence du corpus.

---

## Niveau de transcription

Nous adoptons une transcription **diplomatique** : le texte est reproduit tel qu'il apparaît
dans le document original, sans modernisation de l'orthographe ni résolution des abréviations,
sauf indication contraire ci-dessous.

- Conserver les graphies historiques (`ſ` long s, `v`/`u`, `i`/`j`).
- Ne pas corriger les fautes du scribe.
- Respecter la casse originale.

---

## Abréviations

| Situation | Règle | Exemple |
|-----------|-------|---------|
| Abréviation non résolvable | Transcrire tel quel | `Bn` |
| Abréviation résolvable avec certitude | Développer entre crochets | `B[aptis]me` |
| Mot partiellement illisible | Utiliser `[...]` | `Mar[...]` |

---

## Lacunes

- **Trou physique** dans le papier : `[†]`
- **Tache** rendant le texte illisible : `[illisible]`
- **Texte barré** par le scribe : `~~texte~~`
- **Interlinéaire / ajout** : `^texte^`

---

## Casse

- Conserver les majuscules originales en début de nom propre et en début de paragraphe.
- Ne pas capitaliser les mots qui ne le sont pas dans le document.
- Les en-têtes de colonnes dans les recensements : transcrire en majuscules si écrit ainsi.

---

## Chiffres et nombres

- Transcrire les chiffres romains tels quels : `XVII`, `iij`.
- Les chiffres arabes sont transcrits normalement.
- Séparateurs : utiliser le point comme dans l'original (ne pas moderniser en virgule).

---

## Caractères spéciaux

| Caractère | Unicode | Description |
|-----------|---------|-------------|
| `ſ` | U+017F | S long |
| `&` | U+0026 | Et commercial (esperluette) |
| `æ` | U+00E6 | Ligature ae |
| `œ` | U+0153 | Ligature oe |
