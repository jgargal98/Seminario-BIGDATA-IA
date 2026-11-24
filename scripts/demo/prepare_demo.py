"""
Prepare the demo working folder for a given level.

The folder lives OUTSIDE the repository, next to it (../seminario-demo), so Claude
cannot climb up and read what later levels add (CLAUDE.md, Skills, the project's
Python environment). Each level only has what that level gives it.

Levels are CUMULATIVE:
    1  the data and a plain Python environment with pandas (no DuckDB): only the prompt
    2  + CLAUDE.md, and the project's environment (DuckDB and the rest)
    3  + Skills (.claude/skills/)
    4  + MCP servers (.mcp.json: DuckDB read-only and Hugging Face)

Usage (from the repository root):
    uv run scripts/demo/prepare_demo.py --level 1
    cd ../seminario-demo
    claude

Every run EMPTIES the demo folder, so the demo can restart from scratch.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Shared settings live one folder up, in scripts/common.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import DATABASE_PATH, PARQUET_PATH, ROOT, mcp_config

SESSION = ROOT.parent / "seminario-demo"
LEVELS = ROOT / "demo" / "levels"

# Level files say <repositorio> wherever a command needs the repository; it is
# replaced by its real path so the commands work from the demo folder.
REPO_PLACEHOLDER = "<repositorio>"

# What anyone would have for a quick analysis: pandas, but not DuckDB.
LEVEL1_PACKAGES = ["pandas", "pyarrow"]

DESCRIPTION = {
    1: "los datos y Python con pandas (solo el prompt)",
    2: "+ CLAUDE.md y el entorno del proyecto",
    3: "+ Skills",
    4: "+ MCP",
}


def empty_session():
    """Empty the folder instead of deleting it: a terminal sitting inside it locks the folder itself on Windows."""
    SESSION.mkdir(parents=True, exist_ok=True)
    try:
        for item in SESSION.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    except PermissionError:
        # A file is still open, usually because Claude Code is running in the demo folder.
        raise SystemExit(
            f"No se puede preparar el nivel: hay ficheros de {SESSION.name} en uso.\n"
            "Cierra Claude Code (escribe /exit) y vuelve a ejecutar este comando."
        )


def copy_level_file(source, destination):
    """Copy a CLAUDE.md or SKILL.md, pointing its commands at this repository."""
    text = source.read_text(encoding="utf-8").replace(REPO_PLACEHOLDER, ROOT.as_posix())
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")


def create_plain_python():
    """Level 1: a virtual environment with pandas only, built from uv's cache when possible."""
    uv = shutil.which("uv")
    if not uv:
        raise SystemExit("No se encuentra uv. Ejecuta antes: uv run scripts/install/check_setup.py")
    venv = SESSION / ".venv"
    subprocess.run([uv, "venv", "--quiet", "--python", "3.12", str(venv)], check=True)
    install = [uv, "pip", "install", "--quiet", "--python", str(venv), *LEVEL1_PACKAGES]
    # The project already installed these packages, so the cache usually has them.
    if subprocess.run([*install, "--offline"], capture_output=True).returncode != 0:
        subprocess.run(install, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--level", type=int, choices=range(1, 5), required=True)
    args = parser.parse_args()

    if not DATABASE_PATH.exists() or not PARQUET_PATH.exists():
        raise SystemExit("Faltan los datos. Ejecuta antes: uv run scripts/install/check_setup.py")

    empty_session()
    (SESSION / "queries").mkdir()
    (SESSION / "data").mkdir()
    shutil.copy(PARQUET_PATH, SESSION / "data" / PARQUET_PATH.name)
    shutil.copy(DATABASE_PATH, SESSION / "data" / DATABASE_PATH.name)

    if args.level == 1:
        create_plain_python()
    if args.level >= 2:
        copy_level_file(LEVELS / "level2" / "CLAUDE.md", SESSION / "CLAUDE.md")
    if args.level >= 3:
        for skill in (LEVELS / "level3").rglob("SKILL.md"):
            copy_level_file(skill, SESSION / skill.relative_to(LEVELS / "level3"))
    if args.level >= 4:
        config = mcp_config(SESSION / "data" / DATABASE_PATH.name)
        (SESSION / ".mcp.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    print(f"{SESSION.name} lista para el nivel {args.level}: {DESCRIPTION[args.level]}")
    print(f"Carpeta: {SESSION}")
    print(f"Siguiente paso, en la terminal de la demo: cd {SESSION}  y después  claude")
    if args.level >= 4:
        print("Claude Code pedirá aprobar los servidores MCP del proyecto: acéptalos y comprueba con /mcp.")


if __name__ == "__main__":
    main()
