"""
Create the .mcp.json file that connects Claude Code with your DuckDB database.

The DuckDB MCP server needs the ABSOLUTE path of the database, which differs on
every computer. That is why .mcp.json is generated locally and never committed:
repositories ship .mcp.json.example plus this script.

Usage (from the folder where you will run `claude`):
    uv run scripts/configure_mcp.py
    uv run scripts/configure_mcp.py --db data/analysis.duckdb --dest .
"""

import argparse
import json
from pathlib import Path

from common import DATABASE_PATH, mcp_config


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", default=str(DATABASE_PATH))
    parser.add_argument("--dest", default=".", help="folder where .mcp.json is created")
    parser.add_argument("--max-rows", type=int, default=200, help="maximum rows per MCP answer")
    args = parser.parse_args()

    database = Path(args.db).resolve()
    if not database.exists():
        raise SystemExit(f"No existe {database}. Prepara antes los datos.")
    destination = Path(args.dest).resolve() / ".mcp.json"
    destination.write_text(json.dumps(mcp_config(database, args.max_rows), indent=2) + "\n", encoding="utf-8")
    print(f"Creado {destination}")
    print("  DuckDB se abre en solo lectura (es la opción por defecto del servidor).")
    print("  Siguiente paso: abre `claude` en esa carpeta, aprueba los servidores y comprueba con /mcp.")


if __name__ == "__main__":
    main()
