"""
Run every query in queries/ and check that the results do not change.

This is what lets SOMEONE ELSE reproduce your analysis:

    uv run scripts/demo/reproduce.py           # run, save results and fingerprints
    uv run scripts/demo/reproduce.py --check   # run and compare with saved fingerprints

Rules for a reproducible query:
  * every query has a complete ORDER BY (without it, row order may change);
  * no absolute paths and no unseeded random functions;
  * numbers are rounded in the SQL itself.

Paths are relative to the folder the script is launched from, so the same script
works for the demo session and for a student's own repository.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import duckdb

# Shared settings live one folder up, in scripts/common.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import DATABASE_PATH

HERE = Path.cwd()
QUERIES = HERE / "queries"
RESULTS = HERE / "results"
FINGERPRINTS = RESULTS / "fingerprints.json"


def find_database():
    candidates = [HERE / "data/analysis.duckdb", HERE / "../../data/analysis.duckdb", DATABASE_PATH]
    return next((c.resolve() for c in candidates if c.exists()), candidates[0])


def fingerprint(csv_text):
    return hashlib.sha256(csv_text.encode("utf-8")).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", default=str(find_database()))
    parser.add_argument("--check", action="store_true", help="compare with results/fingerprints.json")
    args = parser.parse_args()

    if not Path(args.db).exists():
        print(f"[FALLO] No existe {args.db}. Ejecuta antes el script de descarga de datos.")
        return 2
    query_files = sorted(QUERIES.glob("*.sql"))
    if not query_files:
        print("[FALLO] No hay consultas en queries/*.sql")
        return 2

    expected = {}
    if args.check:
        if not FINGERPRINTS.exists():
            print("[FALLO] No existe results/fingerprints.json: el autor debe ejecutar antes sin --check")
            return 2
        expected = json.loads(FINGERPRINTS.read_text(encoding="utf-8"))

    RESULTS.mkdir(exist_ok=True)
    current, failures = {}, 0
    with duckdb.connect(args.db, read_only=True) as connection:
        for query_file in query_files:
            name = query_file.stem
            try:
                frame = connection.sql(query_file.read_text(encoding="utf-8")).df()
            except Exception as error:
                print(f"[FALLO] {name}: error al ejecutar -> {str(error).splitlines()[0][:120]}")
                failures += 1
                continue
            csv_text = frame.to_csv(index=False, lineterminator="\n")
            (RESULTS / f"{name}.csv").write_text(csv_text, encoding="utf-8")
            current[name] = fingerprint(csv_text)
            if not args.check:
                print(f"[ OK  ] {name}: {len(frame)} filas -> results/{name}.csv")
            elif expected.get(name) == current[name]:
                print(f"[ OK  ] {name}: coincide ({len(frame)} filas)")
            else:
                print(f"[FALLO] {name}: NO coincide con la huella del autor")
                failures += 1

    if args.check:
        missing = sorted(set(expected) - set(current))
        for name in missing:
            print(f"[FALLO] {name}: está en las huellas pero no en queries/")
        failures += len(missing)
        print("\nREPRODUCIBLE" if failures == 0 else f"\nNO REPRODUCIBLE ({failures} problema/s)")
    elif failures == 0:
        FINGERPRINTS.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
        print("Huellas guardadas en results/fingerprints.json (súbelas con tu entrega)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
