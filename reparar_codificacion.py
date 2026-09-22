from pathlib import Path
import shutil

ROOT = Path(".").resolve()
BACKUP = ROOT / "BACKUP_CODIFICACION"

EXTENSIONES = {
    ".py", ".json", ".js", ".html", ".css",
    ".md", ".txt", ".toml", ".yaml", ".yml"
}

MOJIBAKE = (
    "Ã", "Â", "â", "ð", "�"
)

def score(text):
    return sum(text.count(x) for x in MOJIBAKE)

cambiados = 0
revisados = 0

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in EXTENSIONES:
        continue

    if any(
        parte in path.parts
        for parte in {".git", ".venv", "__pycache__", "BACKUP_CODIFICACION"}
    ):
        continue

    try:
        original = path.read_text(encoding="utf-8")
    except Exception:
        continue

    revisados += 1
    antes = score(original)

    if antes == 0:
        continue

    try:
        corregido = original.encode("latin1").decode("utf-8")
    except Exception:
        continue

    despues = score(corregido)

    if despues < antes:
        relativo = path.relative_to(ROOT)
        destino = BACKUP / relativo
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destino)

        path.write_text(corregido, encoding="utf-8", newline="")
        cambiados += 1

        print(f"CORREGIDO: {relativo}")

print("")
print(f"Archivos revisados : {revisados}")
print(f"Archivos corregidos: {cambiados}")
print(f"Backup             : {BACKUP}")
