import requests
import time
from pathlib import Path

REGISTERS = [
    {"name": "GG20", "ark": "3398221", "label": "accoules_1703"},
    {"name": "GG50", "ark": "3398251", "label": "accoules_1733"},
    {"name": "GG80", "ark": "3398281", "label": "accoules_1763"},
    {"name": "GG109", "ark": "3398310", "label": "accoules_1792"},
]

session = requests.Session()
session.headers.update({"User-Agent": "HTR-Paroisses-Marseille/0.1"})

for reg in REGISTERS:
    print(f"\n=== Téléchargement {reg['name']} ===")
    manifest_url = f"https://archives.marseille.fr/ark:/82766/{reg['ark']}/manifest"
    m = session.get(manifest_url, timeout=30).json()
    canvases = m["sequences"][0]["canvases"]
    total = len(canvases)
    print(f"Pages trouvées : {total}")

    out = Path(f"data/raw/paroissiaux/{reg['name']}")
    out.mkdir(parents=True, exist_ok=True)

    for i, c in enumerate(canvases):
        url = c["images"][0]["resource"]["@id"]
        dest = out / f"{reg['name']}_{reg['label']}_f{i+1:04d}.jpg"
        if dest.exists():
            print(f"[{i+1}/{total}] Skip {dest.name}")
            continue
        try:
            r = session.get(url, timeout=60)
            r.raise_for_status()
            dest.write_bytes(r.content)
            print(f"[{i+1}/{total}] OK {dest.name} ({len(r.content)//1024} Ko)")
        except Exception as e:
            print(f"[{i+1}/{total}] ERREUR : {e}")
        time.sleep(1)

    done = len(list(out.glob("*.jpg")))
    print(f"=== {reg['name']} terminé : {done}/{total} fichiers ===")
    time.sleep(3)

print("\nCORPUS COMPLET")
