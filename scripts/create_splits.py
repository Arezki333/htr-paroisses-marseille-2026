"""Répartition stratifiée des images en splits train / val / test.

Stratégie : shuffle aléatoire intra-registre (seed=42) puis découpe 70/15/15.
Chaque registre contribue proportionnellement aux trois splits, ce qui empêche
la fuite de données inter-registres tout en maintenant la diversité de chaque split.
"""

import hashlib
import json
import random
from pathlib import Path

# ── Constantes ────────────────────────────────────────────────────────────────

SEED = 42
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
# test_ratio implicite : 1 - TRAIN_RATIO - VAL_RATIO = 0.15

BASE_DIR = Path("data/raw/paroissiaux")
SPLITS_DIR = Path("data/splits")

# Périodes approximatives de chaque registre (pour la métadonnée JSON)
REGISTER_PERIODS = {
    "GG1":   "1586-1612",
    "GG20":  "1700-1710",
    "GG50":  "1730-1740",
    "GG80":  "1760-1770",
    "GG109": "1789-1793",
}

# ── Fonctions ─────────────────────────────────────────────────────────────────


def collect_images(base_dir: Path) -> dict[str, list[Path]]:
    """Collecte les images par registre en excluant les sous-dossiers covers/.

    Args:
        base_dir: Racine du dossier des registres bruts.

    Returns:
        Dict {nom_registre: [Path, ...]} trié par registre puis par nom de fichier.
    """
    by_register: dict[str, list[Path]] = {}
    for reg in sorted(REGISTER_PERIODS.keys()):
        reg_dir = base_dir / reg
        if not reg_dir.exists():
            print(f"  Avertissement : {reg_dir} introuvable — registre ignoré.")
            continue
        # Exclure explicitement les fichiers dans covers/
        jpgs = sorted(
            f for f in reg_dir.glob("*.jpg")
            if f.parent == reg_dir  # pas dans un sous-dossier
        )
        by_register[reg] = jpgs
        print(f"  {reg:6s} : {len(jpgs):4d} images")
    return by_register


def split_register(
    files: list[Path], rng: random.Random
) -> tuple[list[Path], list[Path], list[Path]]:
    """Découpe une liste de fichiers en train / val / test après shuffle.

    Args:
        files: Liste de chemins pour un registre.
        rng: Générateur aléatoire déjà seedé.

    Returns:
        Triplet (train, val, test) de listes de Path.
    """
    shuffled = files[:]
    rng.shuffle(shuffled)

    n = len(shuffled)
    n_train = int(n * TRAIN_RATIO)
    n_val = int(n * VAL_RATIO)
    # Le reste va en test pour absorber les arrondis
    return (
        shuffled[:n_train],
        shuffled[n_train : n_train + n_val],
        shuffled[n_train + n_val :],
    )


def make_entry(path: Path, register: str) -> dict:
    """Construit un enregistrement JSON pour une image.

    Args:
        path: Chemin complet de l'image.
        register: Nom du registre (ex. 'GG1').

    Returns:
        Dict avec les clés 'file', 'register', 'period'.
    """
    return {
        "file": f"{register}/{path.name}",
        "register": register,
        "period": REGISTER_PERIODS[register],
    }


def sha256_of_split(entries: list[dict]) -> str:
    """Calcule le SHA-256 canonique d'un split pour la traçabilité.

    Le hash est calculé sur la représentation JSON triée des entrées
    (indépendant de l'ordre d'insertion).

    Args:
        entries: Liste de dicts d'entrées du split.

    Returns:
        Digest SHA-256 hexadécimal (str).
    """
    canonical = json.dumps(
        sorted(entries, key=lambda e: e["file"]),
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    SPLITS_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    print("=" * 60)
    print("Création des splits train / val / test")
    print(f"Seed : {SEED}  |  Ratios : {TRAIN_RATIO:.0%} / {VAL_RATIO:.0%} / {1-TRAIN_RATIO-VAL_RATIO:.0%}")
    print("=" * 60)

    print("\nCollecte des images (hors covers/) :")
    by_register = collect_images(BASE_DIR)

    if not by_register:
        print("\nErreur : aucun registre trouvé. Vérifiez que les images sont dans data/raw/paroissiaux/.")
        return

    train_all: list[dict] = []
    val_all:   list[dict] = []
    test_all:  list[dict] = []

    print("\nRépartition par registre :")
    print(f"  {'Registre':8s}  {'Train':>6}  {'Val':>6}  {'Test':>6}  {'Total':>6}")
    print(f"  {'-'*8}  {'-'*6}  {'-'*6}  {'-'*6}  {'-'*6}")

    for reg, files in by_register.items():
        tr, va, te = split_register(files, rng)
        print(f"  {reg:8s}  {len(tr):6d}  {len(va):6d}  {len(te):6d}  {len(files):6d}")
        train_all.extend(make_entry(f, reg) for f in tr)
        val_all.extend(make_entry(f, reg) for f in va)
        test_all.extend(make_entry(f, reg) for f in te)

    # ── Sauvegarde ────────────────────────────────────────────────────────────
    print()
    for split_name, data in [("train", train_all), ("val", val_all), ("test", test_all)]:
        dest = SPLITS_DIR / f"{split_name}.json"
        dest.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Sauvegardé : {dest}  ({len(data)} entrées)")

    # ── Hash SHA-256 du test set ──────────────────────────────────────────────
    test_hash = sha256_of_split(test_all)
    print(f"\nSHA-256 du test set : {test_hash}")
    print(f"  Basé sur {len(test_all)} entrées — seed={SEED}")

    # ── Résumé global ─────────────────────────────────────────────────────────
    total = len(train_all) + len(val_all) + len(test_all)
    print(f"\nRésumé global :")
    print(f"  Train : {len(train_all):4d}  ({len(train_all)/total:.1%})")
    print(f"  Val   : {len(val_all):4d}  ({len(val_all)/total:.1%})")
    print(f"  Test  : {len(test_all):4d}  ({len(test_all)/total:.1%})")
    print(f"  Total : {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()
