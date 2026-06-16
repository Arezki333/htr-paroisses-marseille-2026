"""Téléchargement du registre paroissial GG1 — Notre-Dame des Accoules (Marseille).

Registre GG1 : 240 vues, 1594–1612.
Source : Archives Municipales de Marseille (domaine public).

Usage :
    python scripts/download_GG1.py
    python scripts/download_GG1.py --output data/raw/paroissiaux/GG1 --delay 1.5
"""

import argparse
import sys
from pathlib import Path

# Ajouter la racine du projet au path pour les imports src.*
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.downloader import download_register
from src.utils.logger import get_logger

# ── Constantes du registre GG1 ────────────────────────────────────────────────

MANIFEST_URL = "https://archives.marseille.fr/ark:/82766/3398202/manifest"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "paroissiaux" / "GG1"
FILE_PREFIX = "GG1_accoules"
EXPECTED_PAGES = 240

# ─────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Télécharge les 240 pages du registre GG1 (Notre-Dame des Accoules) "
                    "depuis les Archives Municipales de Marseille via l'API IIIF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Dossier de destination des images JPEG.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Délai en secondes entre chaque téléchargement (courtoisie serveur).",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=MANIFEST_URL,
        help="URL du manifeste IIIF (avancé — ne modifier que si l'ark change).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logger = get_logger(__name__)

    logger.info("=" * 60)
    logger.info("HTR Paroisses Marseille — Téléchargement GG1")
    logger.info("Manifeste : %s", args.manifest)
    logger.info("Destination : %s", args.output)
    logger.info("Délai entre requêtes : %.1f s", args.delay)
    logger.info("Pages attendues : %d", EXPECTED_PAGES)
    logger.info("=" * 60)

    stats = download_register(
        manifest_url=args.manifest,
        output_dir=args.output,
        prefix=FILE_PREFIX,
        delay=args.delay,
    )

    # ── Rapport final ──────────────────────────────────────────────────────
    logger.info("")
    logger.info("─── Rapport GG1 ───────────────────────────────────────────")
    logger.info("Total dans le manifeste : %d (attendu : %d)", stats["total"], EXPECTED_PAGES)
    logger.info("Nouvellement téléchargées : %d", stats["downloaded"])
    logger.info("Déjà présentes (skip)    : %d", stats["skipped"])
    logger.info("Erreurs                  : %d", stats["errors"])

    if stats["total"] != EXPECTED_PAGES:
        logger.warning(
            "Attention : le manifeste contient %d pages au lieu de %d attendues.",
            stats["total"],
            EXPECTED_PAGES,
        )

    if stats["errors"] > 0:
        logger.warning(
            "Relancer le script pour retenter les %d page(s) en erreur "
            "(les fichiers existants seront ignorés).",
            stats["errors"],
        )
        return 1  # code de sortie non-zéro pour les pipelines CI

    logger.info("Téléchargement GG1 terminé sans erreur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
