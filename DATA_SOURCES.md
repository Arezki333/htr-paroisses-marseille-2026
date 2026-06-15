# Sources de données

## Archives Municipales de Marseille

| Attribut | Valeur |
|----------|--------|
| URL | https://archives.marseille.fr |
| Fonds utilisés | GG 1–663 (registres paroissiaux, 1586–1793) ; recensements 1792–1946 |
| Volume total disponible | > 276 000 images numérisées |
| Format d'image | JPEG / TIFF haute résolution |
| Licence | Domaine public (antérieur à 1900) |
| Accès | Libre, sans inscription, via le formulaire de recherche en ligne |

Images téléchargées stockées dans `data/raw/` (non versionnées — voir `.gitignore`).

---

## HTR-United

| Attribut | Valeur |
|----------|--------|
| URL | https://github.com/HTR-United/htr-united |
| Description | Catalogue de jeux de données d'entraînement HTR documentés et ouverts |
| Jeux utilisés | CATMuS Medieval, CREMMA Medieval, SocFace (si disponible) |
| Licence | CC BY 4.0 (variable selon le jeu) |
| Localisation locale | `ground_truth/htr_united/` |

---

## CATMuS Medieval

| Attribut | Valeur |
|----------|--------|
| Source | HuggingFace — `CATMuS/medieval-htr` |
| Langues | Latin, français médiéval |
| Volume | ~50 000 lignes annotées |
| Période | XIe–XVe siècle |
| Licence | CC BY 4.0 |
| Usage dans le projet | Pré-entraînement / baseline Kraken |

---

## Licences

| Ressource | Licence | Conditions d'utilisation |
|-----------|---------|--------------------------|
| Images AMM | Domaine public | Citer la source : "Archives Municipales de Marseille" |
| CATMuS Medieval | CC BY 4.0 | Attribution obligatoire |
| CREMMA Medieval | CC BY 4.0 | Attribution obligatoire |
| Code du projet | MIT | — |
| Ground truth annoté (projet) | CC BY 4.0 | Attribution obligatoire |

**Toute réutilisation** des données annotées doit mentionner ce projet et les sources originales.
