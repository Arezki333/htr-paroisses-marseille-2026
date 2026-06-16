"""Téléchargement d'images IIIF depuis les Archives Municipales de Marseille.

Supporte le protocole IIIF Presentation API 2.x / 3.x.
Tolérant aux interruptions : les fichiers déjà présents sont ignorés.
"""

import time
from pathlib import Path

import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)

_SESSION_HEADERS = {
    "User-Agent": "HTR-Paroisses-Marseille/0.1 (recherche academique HETIC; contact: hassan.arezki@hetic.eu)",
    "Accept": "image/jpeg,image/*;q=0.9",
}

DEFAULT_DELAY = 1.0
REQUEST_TIMEOUT = 60


def fetch_manifest(manifest_url: str, session: requests.Session | None = None) -> dict:
    """Récupère et parse un manifeste IIIF depuis son URL.

    Args:
        manifest_url: URL complète du manifeste JSON-LD.
        session: Session requests réutilisable (créée si None).

    Returns:
        Manifeste parsé (dict).

    Raises:
        requests.HTTPError: Si le serveur retourne un code d'erreur HTTP.
        requests.ConnectionError: Si le serveur est injoignable.
        ValueError: Si la réponse n'est pas un JSON valide.
    """
    s = session or requests.Session()
    s.headers.update(_SESSION_HEADERS)

    logger.info("Récupération du manifeste : %s", manifest_url)
    resp = s.get(manifest_url, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()

    try:
        manifest = resp.json()
    except ValueError as exc:
        raise ValueError(f"Le manifeste n'est pas un JSON valide : {manifest_url}") from exc

    logger.info(
        "Manifeste chargé — label : %s",
        manifest.get("label", "<sans label>"),
    )
    return manifest


def extract_image_urls(manifest: dict) -> list[dict]:
    """Extrait les URLs d'images depuis un manifeste IIIF Presentation API 2.x.

    Pour chaque canvas, tente d'utiliser l'URL de service IIIF Image API
    (qualité maximale) ; replie sur l'URL directe de la ressource.

    Args:
        manifest: Manifeste IIIF parsé (dict).

    Returns:
        Liste de dicts ordonnés avec les clés :
            - ``index`` (int) : position 0-based dans le manifeste.
            - ``label`` (str) : label du canvas.
            - ``image_url`` (str) : URL IIIF Image API en qualité max.

    Raises:
        KeyError: Si le manifeste ne suit pas la structure IIIF Presentation 2.x.
    """
    try:
        canvases = manifest["sequences"][0]["canvases"]
    except (KeyError, IndexError) as exc:
        raise KeyError(
            "Structure IIIF Presentation 2.x attendue (sequences[0].canvases introuvable)"
        ) from exc

    images = []
    for i, canvas in enumerate(canvases):
        try:
            resource = canvas["images"][0]["resource"]
        except (KeyError, IndexError):
            logger.warning("Canvas %d : ressource image introuvable, ignoré.", i)
            continue

        # Priorité : URL du service IIIF → qualité /full/max/0/default.jpg
        service = resource.get("service", {})
        if isinstance(service, list):
            service = service[0] if service else {}
        service_id = (service.get("@id") or service.get("id") or "").rstrip("/")

        if service_id:
            image_url = f"{service_id}/full/max/0/default.jpg"
        else:
            # Repli sur l'URL directe de la ressource (peut être une URL complète)
            image_url = resource.get("@id", resource.get("id", ""))

        label = canvas.get("label", f"page_{i:04d}")
        # label peut être une str ou un dict langmap {"fr": "..."}
        if isinstance(label, dict):
            label = next(iter(label.values()), f"page_{i:04d}")

        images.append({"index": i, "label": str(label), "image_url": image_url})

    logger.info("%d image(s) extraite(s) du manifeste.", len(images))
    return images


def _build_dest_path(output_dir: Path, prefix: str, index: int) -> Path:
    """Construit le chemin de destination d'une image téléchargée.

    Args:
        output_dir: Dossier de sortie.
        prefix: Préfixe du nom de fichier (ex. 'GG1_accoules').
        index: Index 0-based de la page dans le manifeste.

    Returns:
        Chemin complet du fichier JPEG de destination.
    """
    # Convention archivistique : folio numéroté à partir de 1, 4 chiffres
    folio = index + 1
    return output_dir / f"{prefix}_f{folio:04d}.jpg"


def download_image(
    url: str,
    dest_path: Path,
    session: requests.Session,
) -> bool:
    """Télécharge une image depuis une URL IIIF vers un fichier local.

    Args:
        url: URL de l'image (IIIF Image API ou URL directe).
        dest_path: Chemin de destination (le dossier parent est créé si absent).
        session: Session requests à réutiliser.

    Returns:
        True si le téléchargement a réussi.

    Raises:
        requests.HTTPError: Si le serveur retourne une erreur HTTP.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    resp = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
    resp.raise_for_status()

    with dest_path.open("wb") as fh:
        for chunk in resp.iter_content(chunk_size=8_192):
            fh.write(chunk)
    return True


def download_register(
    manifest_url: str,
    output_dir: Path,
    prefix: str = "GG1_accoules",
    delay: float = DEFAULT_DELAY,
) -> dict:
    """Télécharge toutes les images d'un registre depuis son manifeste IIIF.

    Reprend automatiquement là où le téléchargement s'est arrêté :
    les fichiers déjà présents sur le disque sont ignorés.

    Args:
        manifest_url: URL complète du manifeste IIIF.
        output_dir: Dossier de destination des images.
        prefix: Préfixe des noms de fichiers générés.
        delay: Délai en secondes entre chaque requête (courtoisie serveur).

    Returns:
        Dictionnaire de statistiques :
            - ``total`` (int) : nombre total d'images dans le manifeste.
            - ``downloaded`` (int) : images nouvellement téléchargées.
            - ``skipped`` (int) : images déjà présentes (skip).
            - ``errors`` (int) : échecs de téléchargement.
            - ``error_indices`` (list[int]) : indices des pages en erreur.
    """
    output_dir = Path(output_dir)
    stats = {"total": 0, "downloaded": 0, "skipped": 0, "errors": 0, "error_indices": []}

    session = requests.Session()
    session.headers.update(_SESSION_HEADERS)

    manifest = fetch_manifest(manifest_url, session=session)
    images = extract_image_urls(manifest)
    stats["total"] = len(images)

    logger.info(
        "Début du téléchargement — %d image(s) → %s", stats["total"], output_dir
    )

    for entry in images:
        idx = entry["index"]
        dest = _build_dest_path(output_dir, prefix, idx)

        if dest.exists():
            logger.debug("Déjà présent, ignoré : %s", dest.name)
            stats["skipped"] += 1
            continue

        folio = idx + 1
        logger.info("[%d/%d] Téléchargement : %s", folio, stats["total"], dest.name)

        try:
            download_image(entry["image_url"], dest, session)
            stats["downloaded"] += 1
        except requests.RequestException as exc:
            logger.error("Erreur folio %d : %s", folio, exc)
            stats["errors"] += 1
            stats["error_indices"].append(idx)
        finally:
            time.sleep(delay)

    logger.info(
        "Terminé — téléchargées : %d | ignorées : %d | erreurs : %d",
        stats["downloaded"],
        stats["skipped"],
        stats["errors"],
    )
    if stats["error_indices"]:
        logger.warning("Pages en erreur (index 0-based) : %s", stats["error_indices"])

    return stats
