"""
Prepare the demo working folder (demo/session/) for a given level.

Levels are CUMULATIVE:
    1  empty folder: only the prompt changes
    2  + CLAUDE.md
    3  + Skills (.claude/skills/)
    4  + MCP servers (.mcp.json: DuckDB read-only and Hugging Face)

Usage:
    uv run scripts/demo/prepare_demo.py --level 2
    cd demo/session
    claude

Every run DELETES and recreates demo/session/, so the demo can restart from scratch.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# Shared settings live one folder up, in scripts/common.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import DATABASE_PATH, ROOT, mcp_config

SESSION = ROOT / "demo" / "session"
LEVELS = ROOT / "demo" / "levels"

DESCRIPTION = {
    1: "nada (solo el prompt)",
    2: "CLAUDE.md",
    3: "CLAUDE.md + Skills",
    4: "CLAUDE.md + Skills + MCP",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--level", type=int, choices=range(1, 5), required=True)
    args = parser.parse_args()

    if not DATABASE_PATH.exists():
        raise SystemExit("Faltan los datos. Ejecuta antes: uv run scripts/install/check_setup.py")

    if SESSION.exists():
        shutil.rmtree(SESSION)
    (SESSION / "queries").mkdir(parents=True)

    if args.level >= 2:
        shutil.copy(LEVELS / "level2" / "CLAUDE.md", SESSION / "CLAUDE.md")
    if args.level >= 3:
        shutil.copytree(LEVELS / "level3" / ".claude", SESSION / ".claude")
    if args.level >= 4:
        (SESSION / ".mcp.json").write_text(json.dumps(mcp_config(DATABASE_PATH), indent=2) + "\n", encoding="utf-8")

    print(f"demo/session/ lista para el nivel {args.level}: {DESCRIPTION[args.level]}")
    print("Siguiente paso: cd demo/session  y después  claude")
    if args.level >= 4:
        print("Claude Code pedirá aprobar los servidores MCP del proyecto: acéptalos y comprueba con /mcp.")


if __name__ == "__main__":
    main()
