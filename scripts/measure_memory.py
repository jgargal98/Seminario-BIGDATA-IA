"""
Measure peak memory and time of the same aggregation done in different ways.

Every method computes the median yearly salary per job title, each one in its
own process so its peak memory (RSS) can be measured on its own.

Usage:
    uv run scripts/measure_memory.py
    uv run scripts/measure_memory.py --csv path/to/file.csv --parquet data/jobs.parquet
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

import duckdb
import psutil

from common import DATA_DIR, PARQUET_PATH

QUERY = "SELECT job_title_short, median(salary_year_avg) FROM {source} GROUP BY 1"

METHODS = {
    "pandas, CSV completo en memoria": """
import pandas as pd
frame = pd.read_csv(r'{csv}', low_memory=False)
print(len(frame.groupby('job_title_short')['salary_year_avg'].median()))
""",
    "pandas, Parquet solo 2 columnas": """
import pandas as pd
frame = pd.read_parquet(r'{parquet}', columns=['job_title_short', 'salary_year_avg'])
print(len(frame.groupby('job_title_short')['salary_year_avg'].median()))
""",
    "DuckDB sobre el CSV": """
import duckdb
print(len(duckdb.sql(\"\"\"{query_csv}\"\"\").fetchall()))
""",
    "DuckDB sobre el Parquet": """
import duckdb
print(len(duckdb.sql(\"\"\"{query_parquet}\"\"\").fetchall()))
""",
}


def tree_rss(process):
    """Resident memory of a process plus its children.

    On Windows the venv python.exe is a launcher that starts the real interpreter
    as a child, so measuring only the launcher reports a few MB.
    """
    total = 0
    for member in [process, *process.children(recursive=True)]:
        try:
            total += member.memory_info().rss
        except psutil.Error:
            pass
    return total


def measure(code):
    """Run code in a child process, polling its resident memory until it exits."""
    start = time.time()
    process = subprocess.Popen([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    watched = psutil.Process(process.pid)
    peak = 0
    while process.poll() is None:
        try:
            peak = max(peak, tree_rss(watched))
        except psutil.Error:
            break
        time.sleep(0.02)
    output, error = process.communicate()
    if process.returncode != 0:
        return 0.0, time.time() - start, "ERROR: " + (error.strip().splitlines() or ["?"])[-1][:80]
    return peak / 1e6, time.time() - start, output.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--parquet", default=str(PARQUET_PATH))
    parser.add_argument("--csv", help="CSV to measure; generated from the Parquet file if omitted")
    args = parser.parse_args()

    parquet = Path(args.parquet).resolve()
    if not parquet.exists():
        sys.exit(f"No existe {parquet}. Ejecuta antes: uv run scripts/check_setup.py")
    csv = Path(args.csv).resolve() if args.csv else (DATA_DIR / "jobs_measure.csv").resolve()
    if not csv.exists():
        print(f"Generando {csv.name} a partir del Parquet (solo la primera vez)...")
        duckdb.sql(f"COPY (SELECT * FROM '{parquet.as_posix()}') TO '{csv.as_posix()}' (HEADER)")

    values = {
        "csv": csv.as_posix(),
        "parquet": parquet.as_posix(),
        "query_csv": QUERY.format(source=f"read_csv('{csv.as_posix()}', sample_size = 100000)"),
        "query_parquet": QUERY.format(source=f"'{parquet.as_posix()}'"),
    }
    total_ram_gb = psutil.virtual_memory().total / 1e9
    print(f"CSV: {csv.stat().st_size / 1e6:.0f} MB   Parquet: {parquet.stat().st_size / 1e6:.0f} MB   "
          f"RAM del equipo: {total_ram_gb:.1f} GB\n")
    print(f"{'Método':<36}{'Memoria pico':>14}{'Tiempo':>10}")

    pandas_peak = None
    for name, template in METHODS.items():
        memory_mb, seconds, output = measure(template.format(**values))
        note = f"  {output}" if output.startswith("ERROR") else ""
        print(f"{name:<36}{memory_mb:>11,.0f} MB{seconds:>8.1f} s{note}")
        if name.startswith("pandas, CSV") and memory_mb:
            pandas_peak = memory_mb

    if pandas_peak:
        factor = total_ram_gb * 1000 / pandas_peak
        print(f"\nCargando el CSV entero, pandas llenaría la RAM de este equipo con unas {factor:.0f} veces más datos.")
        print("A partir de ahí hay que leer solo lo necesario (columnas, particiones) o repartir el trabajo (Spark).")


if __name__ == "__main__":
    main()
