"""Détection de la reliure et découpe des scans double-page en deux pages séparées.

Algorithme :
  1. Filtre d'aspect : width/height < 1.35 → page unique, ignorer.
  2. Profil de luminosité : moyenne par colonne sur la bande centrale [20%-80%] en hauteur.
  3. Lissage par moyenne glissante (fenêtre 50 px) pour neutraliser le bruit.
  4. Recherche du minimum dans la zone [30%-70%] de la largeur.
  5. Validation : la reliure doit être ≥ 10 niveaux plus sombre que la moyenne globale.
  6. Découpe au pixel de reliure ; sauvegarde en JPEG 95%.
"""

import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# ── Paramètres ────────────────────────────────────────────────────────────────

REGISTERS = ["GG1", "GG20", "GG50", "GG80", "GG109"]

BASE_RAW = Path("data/raw/paroissiaux")
BASE_OUT = Path("data/processed/pages")

# Ratio w/h minimum pour traiter l'image comme un scan double-page
DOUBLE_PAGE_RATIO = 1.20

# Zone centrale de la largeur où chercher la reliure
GUTTER_SEARCH_LEFT  = 0.30
GUTTER_SEARCH_RIGHT = 0.70

# Bande horizontale (fraction de la hauteur) utilisée pour le profil de luminosité
# Les marges supérieure et inférieure sont souvent noires → on les exclut
BAND_TOP    = 0.20
BAND_BOTTOM = 0.80

# Fenêtre de lissage (pixels) du profil de luminosité
SMOOTH_WINDOW = 50

# Différence minimale (niveaux de gris) entre la moyenne et le minimum
# pour valider la présence d'une reliure
GUTTER_MIN_CONTRAST = 10

# Pattern du nom de fichier : GG{n}_{label...}_f{NNNN}.jpg
_RE_FOLIO = re.compile(r"^(GG\d+)_.*_(f\d{4})\.jpg$", re.IGNORECASE)

# ── Fonctions utilitaires ─────────────────────────────────────────────────────


def _smooth(arr: np.ndarray, window: int) -> np.ndarray:
    """Lissage par convolution avec une fenêtre rectangulaire uniforme."""
    kernel = np.ones(window, dtype=np.float32) / window
    return np.convolve(arr, kernel, mode="same")


def detect_gutter(gray: np.ndarray) -> int | None:
    """Renvoie l'index de la colonne de reliure, ou None si non détectée.

    Args:
        gray: Image en niveaux de gris (np.float32, shape H×W).

    Returns:
        Indice de colonne de la reliure, ou None.
    """
    h, w = gray.shape

    # Profil de luminosité : moyenne par colonne sur la bande centrale
    band = gray[int(h * BAND_TOP) : int(h * BAND_BOTTOM), :]
    col_profile = band.mean(axis=0).astype(np.float32)

    # Lissage
    col_smooth = _smooth(col_profile, SMOOTH_WINDOW)

    # Recherche du minimum dans la zone centrale
    left  = int(w * GUTTER_SEARCH_LEFT)
    right = int(w * GUTTER_SEARCH_RIGHT)
    region = col_smooth[left:right]

    local_idx  = int(np.argmin(region))
    gutter_col = left + local_idx

    # Validation par contraste
    mean_val   = float(col_smooth[left:right].mean())
    gutter_val = float(col_smooth[gutter_col])

    if mean_val - gutter_val < GUTTER_MIN_CONTRAST:
        return None  # pas de reliure fiable

    return gutter_col


def is_double_page(width: int, height: int) -> bool:
    """Retourne True si le ratio w/h indique un scan double-page."""
    return (width / height) >= DOUBLE_PAGE_RATIO


def parse_filename(name: str) -> tuple[str, str] | None:
    """Extrait (registre, folio) depuis le nom de fichier.

    Args:
        name: Nom de fichier brut, ex. 'GG20_accoules_1703_f0042.jpg'.

    Returns:
        ('GG20', 'f0042') ou None si le pattern ne correspond pas.
    """
    m = _RE_FOLIO.match(name)
    return (m.group(1), m.group(2)) if m else None


def split_image(img: Image.Image, gutter_col: int) -> tuple[Image.Image, Image.Image]:
    """Découpe une image PIL en deux à la colonne de reliure.

    Args:
        img: Image source (RGB).
        gutter_col: Indice de colonne de la reliure.

    Returns:
        Tuple (page_gauche, page_droite).
    """
    w, h = img.size
    left  = img.crop((0,           0, gutter_col, h))
    right = img.crop((gutter_col,  0, w,          h))
    return left, right


# ── Traitement d'un registre ──────────────────────────────────────────────────


def process_register(register: str, stats: dict) -> None:
    """Traite toutes les images d'un registre et met à jour les statistiques.

    Args:
        register: Nom du registre (ex. 'GG1').
        stats: Dictionnaire de compteurs partagé, modifié en place.
    """
    src_dir = BASE_RAW / register
    out_dir = BASE_OUT / register

    if not src_dir.exists():
        print(f"  {register} : {src_dir} introuvable — ignoré.")
        return

    jpgs = sorted(f for f in src_dir.glob("*.jpg") if f.parent == src_dir)
    if not jpgs:
        print(f"  {register} : aucun fichier .jpg trouvé.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    reg_split = reg_skip = reg_err = 0

    for img_path in jpgs:
        parsed = parse_filename(img_path.name)
        if parsed is None:
            print(f"    Pattern inconnu : {img_path.name} — ignoré.")
            stats["skipped"] += 1
            reg_skip += 1
            continue

        reg_name, folio = parsed

        try:
            img = Image.open(img_path).convert("RGB")
        except Exception as exc:
            print(f"    Erreur lecture {img_path.name} : {exc}")
            stats["errors"] += 1
            reg_err += 1
            continue

        w, h = img.size

        # ── Filtre d'aspect ───────────────────────────────────────────────
        if not is_double_page(w, h):
            print(
                f"    {img_path.name}  {w}×{h}  ratio={w/h:.2f} "
                f"→ page unique, ignorée."
            )
            stats["single_page"] += 1
            reg_skip += 1
            continue

        # ── Détection de la reliure ───────────────────────────────────────
        gray = np.array(img.convert("L"), dtype=np.float32)
        gutter = detect_gutter(gray)

        if gutter is None:
            print(
                f"    {img_path.name}  {w}×{h} "
                f"→ reliure non détectée (contraste insuffisant), ignorée."
            )
            stats["no_gutter"] += 1
            reg_skip += 1
            continue

        # ── Découpe et sauvegarde ─────────────────────────────────────────
        left_img, right_img = split_image(img, gutter)
        lw, lh = left_img.size
        rw, rh = right_img.size

        left_path  = out_dir / f"{reg_name}_{folio}_L.jpg"
        right_path = out_dir / f"{reg_name}_{folio}_R.jpg"

        left_img.save(left_path,  "JPEG", quality=95)
        right_img.save(right_path, "JPEG", quality=95)

        print(
            f"    {img_path.name}  {w}×{h}  reliure=col{gutter} "
            f"→ L:{lw}×{lh}  R:{rw}×{rh}"
        )
        stats["split"] += 1
        reg_split += 1

    print(
        f"  {register} : {reg_split} scindée(s) | "
        f"{reg_skip} ignorée(s) | {reg_err} erreur(s)"
    )


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    print("=" * 68)
    print("split_pages.py — Découpe des scans double-page")
    print(f"Source : {BASE_RAW}")
    print(f"Sortie : {BASE_OUT}")
    print("=" * 68)

    stats = {
        "split":       0,   # images découpées en deux pages
        "single_page": 0,   # ignorées (page unique détectée par le ratio)
        "no_gutter":   0,   # ignorées (reliure non détectée)
        "skipped":     0,   # ignorées (nom de fichier non reconnu)
        "errors":      0,   # erreurs de lecture
    }

    for register in REGISTERS:
        print(f"\n── {register} {'─'*50}")
        process_register(register, stats)

    # ── Résumé ────────────────────────────────────────────────────────────
    total_in  = stats["split"] + stats["single_page"] + stats["no_gutter"] + stats["skipped"]
    total_out = stats["split"] * 2  # chaque scan double-page → 2 fichiers

    print("\n" + "=" * 68)
    print("Résumé")
    print(f"  Images traitées (entrée)         : {total_in}")
    print(f"  Scans double-page découpés       : {stats['split']}  → {total_out} fichiers de sortie")
    print(f"  Ignorées — page unique (ratio)   : {stats['single_page']}")
    print(f"  Ignorées — reliure non détectée  : {stats['no_gutter']}")
    print(f"  Ignorées — nom de fichier inconnu: {stats['skipped']}")
    print(f"  Erreurs de lecture               : {stats['errors']}")
    print(f"  Dossier de sortie                : {BASE_OUT.resolve()}")
    print("=" * 68)

    return 1 if stats["errors"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
