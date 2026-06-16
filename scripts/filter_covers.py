import shutil
from pathlib import Path

REGISTERS = {
    "GG1":   {"first": 2, "last": 2},
    "GG20":  {"first": 2, "last": 2},
    "GG50":  {"first": 2, "last": 2},
    "GG80":  {"first": 2, "last": 2},
    "GG109": {"first": 2, "last": 1},
}

base = Path("data/raw/paroissiaux")

for reg, config in REGISTERS.items():
    reg_dir = base / reg
    covers_dir = reg_dir / "covers"
    covers_dir.mkdir(exist_ok=True)

    all_jpgs = sorted(reg_dir.glob("*.jpg"))
    total = len(all_jpgs)

    to_move = all_jpgs[:config["first"]] + all_jpgs[-config["last"]:]

    for f in to_move:
        dest = covers_dir / f.name
        shutil.move(str(f), str(dest))
        print(f"Déplacé : {f.name} → {reg}/covers/")

    remaining = total - len(to_move)
    print(f"{reg} : {remaining} pages HTR utiles sur {total} totales")
    print()

print("Filtrage terminé.")
