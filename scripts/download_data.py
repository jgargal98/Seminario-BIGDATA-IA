"""
Download a dataset, convert it to Parquet and build the DuckDB database.

Output (data/ folder):
    jobs.parquet      the dataset in columnar format, with a row_id column
    analysis.duckdb   database with the `jobs` table

Examples:
    uv run scripts/download_data.py                                  # demo dataset
    uv run scripts/download_data.py --dataset Yelp/yelp_review_full  # another HF dataset
    uv run scripts/download_data.py --csv my_file.csv                # local file
"""

import argparse
import sys
from pathlib import Path

import duckdb

from common import DATA_DIR, DATABASE_PATH, DEMO_DATASET, PARQUET_PATH, ROOT, TABLE, format_int

SYNTHETIC_CSV = DATA_DIR / "synthetic" / "data_jobs_synthetic.csv"


def download_from_hub(repo, destination, max_files):
    """Fetch the data files of a Hugging Face dataset, preferring Parquet over CSV."""
    from huggingface_hub import hf_hub_download, list_repo_files

    files = list_repo_files(repo, repo_type="dataset")
    parquet = [f for f in files if f.endswith(".parquet")]
    csv = [f for f in files if f.lower().endswith((".csv", ".csv.gz"))]
    chosen = (parquet or csv)[:max_files]
    if not chosen:
        sys.exit(f"No hay ficheros .parquet ni .csv en {repo}. Ficheros: {files[:10]}")
    print(f"  {repo}: {len(parquet)} parquet, {len(csv)} csv. Se descargan {len(chosen)}.")
    paths = []
    for name in chosen:
        print(f"  Descargando {name} (solo la primera vez)...")
        paths.append(Path(hf_hub_download(repo, name, repo_type="dataset", local_dir=destination)))
    return paths


def build(sources, parquet_path=PARQUET_PATH, database_path=DATABASE_PATH, max_rows=None):
    """Write the Parquet file and the DuckDB database; return (rows, columns)."""
    sources_sql = ", ".join(f"'{p.as_posix()}'" for p in sources)
    if sources[0].suffix == ".parquet":
        reader = f"read_parquet([{sources_sql}])"
    else:
        # A large sample avoids wrong type guesses on columns that are mostly NULL.
        reader = f"read_csv([{sources_sql}], sample_size = 100000)"
    limit = f" LIMIT {max_rows}" if max_rows else ""

    parquet_path.parent.mkdir(parents=True, exist_ok=True)
    duckdb.sql(f"""
        COPY (SELECT row_number() OVER () AS row_id, * FROM {reader}{limit})
        TO '{parquet_path.as_posix()}' (FORMAT parquet, COMPRESSION zstd)
    """)

    if database_path.exists():
        database_path.unlink()
    with duckdb.connect(str(database_path)) as connection:
        connection.sql(f"CREATE TABLE {TABLE} AS SELECT * FROM read_parquet('{parquet_path.as_posix()}')")
        rows = connection.sql(f"SELECT count(*) FROM {TABLE}").fetchall()[0][0]
        columns = len(connection.sql(f"DESCRIBE {TABLE}").fetchall())
    return rows, columns


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", default=DEMO_DATASET, help="Hugging Face id (user/name)")
    parser.add_argument("--csv", help="use a local CSV instead of downloading")
    parser.add_argument("--synthetic", action="store_true", help="use the synthetic CSV (offline plan B)")
    parser.add_argument("--max-files", type=int, default=4, help="maximum number of files to download")
    parser.add_argument("--max-rows", type=int, help="keep only the first N rows")
    args = parser.parse_args()

    if args.synthetic:
        args.csv = str(SYNTHETIC_CSV)
    if args.csv:
        sources = [Path(args.csv)]
        if not sources[0].exists():
            sys.exit(f"No existe {args.csv}")
    else:
        sources = download_from_hub(args.dataset, DATA_DIR / "download", args.max_files)

    rows, columns = build(sources, max_rows=args.max_rows)
    source_mb = sum(p.stat().st_size for p in sources) / 1e6
    print(f"  {PARQUET_PATH.relative_to(ROOT).as_posix()}: {PARQUET_PATH.stat().st_size / 1e6:.0f} MB "
          f"(original: {source_mb:.0f} MB)")
    print(f"  {DATABASE_PATH.relative_to(ROOT).as_posix()}: tabla `{TABLE}` con {format_int(rows)} filas y {columns} columnas")
    if rows < 100_000:
        print("  Aviso: menos de 100.000 filas. El ejercicio pide cientos de miles.")


if __name__ == "__main__":
    main()
