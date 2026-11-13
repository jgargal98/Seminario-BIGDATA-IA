"""
Quick profile of a table: rows, columns, types, nulls and sample values.

Usage:
    uv run scripts/profile_dataset.py
    uv run scripts/profile_dataset.py --db data/analysis.duckdb --table jobs --md profile.md
"""

import argparse
from pathlib import Path

import duckdb

from common import DATABASE_PATH, TABLE, format_int


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", default=str(DATABASE_PATH))
    parser.add_argument("--table", default=TABLE)
    parser.add_argument("--md", help="also save the profile as Markdown")
    args = parser.parse_args()

    if not Path(args.db).exists():
        raise SystemExit(f"No existe {args.db}. Ejecuta antes: uv run scripts/check_setup.py")

    with duckdb.connect(args.db, read_only=True) as connection:
        table = args.table
        rows = connection.sql(f"SELECT count(*) FROM {table}").fetchall()[0][0]
        columns = connection.sql(f"DESCRIBE {table}").fetchall()
        # One pass over the table for every column instead of one query per column.
        null_counts = connection.sql(
            "SELECT " + ", ".join(f'count(*) - count("{c[0]}")' for c in columns) + f" FROM {table}"
        ).fetchall()[0]

        lines = [f"# Perfil de `{table}`", "", f"- Filas: **{format_int(rows)}**", f"- Columnas: **{len(columns)}**", ""]
        lines += ["| Columna | Tipo | % nulos | Ejemplo |", "|---|---|---|---|"]
        for (name, column_type, *_), nulls in zip(columns, null_counts):
            sample = connection.sql(f'SELECT "{name}" FROM {table} WHERE "{name}" IS NOT NULL LIMIT 1').fetchall()
            example = str(sample[0][0])[:40].replace("|", "/") if sample else ""
            marker = " (alto)" if rows and nulls / rows > 0.3 else ""
            lines.append(f"| {name} | {column_type} | {100 * nulls / rows:.1f} %{marker} | `{example}` |")

    text = "\n".join(lines)
    print(text)
    if args.md:
        Path(args.md).write_text(text + "\n", encoding="utf-8")
        print(f"\nGuardado en {args.md}")


if __name__ == "__main__":
    main()
