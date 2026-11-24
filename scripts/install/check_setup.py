"""
Setup check for the "Big Data con IA" seminar.

Run with:  uv run scripts/install/check_setup.py
           uv run scripts/install/check_setup.py --offline   (skip everything that needs the network)

Verifies tools and libraries, and downloads everything that would otherwise depend
on the classroom network: demo dataset, AI model and MCP server.
Safe to re-run: anything already downloaded is reused.

Messages are in Spanish because they are aimed at the students.
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Shared settings live one folder up, in scripts/common.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from common import (
    DATABASE_PATH,
    DATA_DIR,
    DEMO_DATASET,
    DUCKDB_MCP_UVX_ARGS,
    REVIEWS_SAMPLE_PATH,
    ROOT,
    SENTIMENT_MODEL,
    TABLE,
    TEXT_DATASET,
    TEXT_DATASET_FILE,
    format_int,
)

REQUIRED_DUCKDB = "1.5.6"
MIN_FREE_GB = 5

results = {"ok": 0, "warning": 0, "failure": 0}


def section(text):
    print(f"\n=== {text} ===")


def report(kind, label, text, fix=None):
    results[kind] += 1
    print(f"  [{label}] {text}")
    if fix:
        print(f"          -> {fix}")


def ok(text):
    report("ok", " OK  ", text)


def warning(text, fix=None):
    report("warning", "AVISO", text, fix)


def failure(text, fix=None):
    report("failure", "FALLO", text, fix)


def check_tools():
    section("1. Programas instalados")
    tools = {
        "git": ("Git", "Instálalo desde el enlace del README y abre una terminal nueva."),
        "claude": ("Claude Code", "Instálalo desde el enlace del README y abre una terminal nueva."),
        "uvx": ("uv / uvx", "Instálalo desde el enlace del README y abre una terminal nueva."),
    }
    for command, (name, fix) in tools.items():
        if shutil.which(command):
            ok(name)
        else:
            failure(f"No se encuentra {name}.", fix)

    ok(f"Python {sys.version.split()[0]} (gestionado por uv)")

    free_gb = shutil.disk_usage(ROOT).free / 1e9
    if free_gb >= MIN_FREE_GB:
        ok(f"Espacio libre: {free_gb:.0f} GB")
    else:
        failure(f"Espacio libre: {free_gb:.1f} GB", f"Libera hasta tener al menos {MIN_FREE_GB} GB.")


def check_libraries():
    section("2. Librerías de Python")
    all_found = True
    for name in ["duckdb", "pandas", "pyarrow", "psutil", "transformers", "torch", "matplotlib", "mcp"]:
        try:
            module = __import__(name)
        except Exception as error:
            all_found = False
            failure(f"No se puede importar {name}: {error}", "Ejecuta: uv sync")
            continue
        version = getattr(module, "__version__", "")
        if name == "duckdb" and version != REQUIRED_DUCKDB:
            all_found = False
            failure(f"duckdb {version}", f"Hace falta la {REQUIRED_DUCKDB} (la del servidor MCP). Ejecuta: uv sync")
        else:
            ok(f"{name} {version}".strip())
    return all_found


def check_remote_read():
    section("3. DuckDB leyendo directamente desde Hugging Face")
    import duckdb

    try:
        connection = duckdb.connect()
        # httpfs is the extension behind hf:// paths. Installing it now avoids
        # a download during the seminar.
        connection.sql("INSTALL httpfs; LOAD httpfs;")
        path = f"hf://datasets/{TEXT_DATASET}/{TEXT_DATASET_FILE}"
        start = time.time()
        total = connection.sql(f"SELECT count(*) FROM '{path}'").fetchall()[0][0]
        ok(f"{format_int(total)} reseñas contadas en {time.time() - start:.1f} s sin descargar el fichero")
    except Exception as error:
        failure(f"DuckDB no ha podido leer desde Hugging Face: {error}", "Revisa tu conexión y vuelve a ejecutar.")


def prepare_demo_data():
    section("4. Datos de la demo (carpeta data/)")
    import duckdb
    from download_data import build, download_from_hub, download_reviews_sample

    try:
        if DATABASE_PATH.exists():
            with duckdb.connect(str(DATABASE_PATH), read_only=True) as connection:
                rows = connection.sql(f"SELECT count(*) FROM {TABLE}").fetchall()[0][0]
            ok(f"Ya preparados: tabla `{TABLE}` con {format_int(rows)} filas")
        else:
            print("  Descargando unos 230 MB (solo la primera vez)...")
            sources = download_from_hub(DEMO_DATASET, DATA_DIR / "download", max_files=1)
            rows, columns = build(sources)
            ok(f"Tabla `{TABLE}` creada: {format_int(rows)} filas, {columns} columnas")
    except Exception as error:
        failure(f"No se han podido preparar los datos: {error}", "Revisa tu conexión y vuelve a ejecutar.")

    try:
        if REVIEWS_SAMPLE_PATH.exists():
            ok(f"Muestra de reseñas ya preparada: {REVIEWS_SAMPLE_PATH.relative_to(ROOT).as_posix()}")
            return
        print("  Sacando una muestra de reseñas de Hugging Face (solo la primera vez, puede tardar unos minutos)...")
        rows = download_reviews_sample()
        ok(f"Muestra de {rows} reseñas guardada en {REVIEWS_SAMPLE_PATH.relative_to(ROOT).as_posix()}")
    except Exception as error:
        failure(f"No se ha podido preparar la muestra de reseñas: {error}", "Revisa tu conexión y vuelve a ejecutar.")


def check_model():
    section("5. Modelo de IA de Hugging Face")
    try:
        print("  Descargando unos 700 MB (solo la primera vez)...")
        from transformers import pipeline

        classifier = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
        positive = classifier("Me encanta, llegó rápido y funciona perfectamente. Muy recomendable.")[0]["label"]
        negative = classifier("Llegó roto y el vendedor no responde. Una estafa, no lo compréis.")[0]["label"]

        # Labels look like "5 stars". Both sentences are deliberately obvious,
        # so a wrong answer means a broken install rather than a model limitation.
        if int(positive.split()[0]) >= 4 and int(negative.split()[0]) <= 2:
            ok(f"Frase positiva: {positive}. Frase negativa: {negative}.")
        else:
            warning(f"El modelo responde, pero con resultados raros: {positive} / {negative}")
    except Exception as error:
        failure(f"No se ha podido cargar el modelo: {error}", "Revisa tu conexión y el espacio en disco.")


def prepare_mcp():
    section("6. Servidores MCP para Claude Code")
    uvx = shutil.which("uvx")
    if uvx:
        # Fetch the server now so its first launch inside Claude Code is instant
        # instead of risking a startup timeout.
        try:
            print("  Preparando el servidor MCP de DuckDB (solo la primera vez)...")
            subprocess.run([uvx, *DUCKDB_MCP_UVX_ARGS, "--help"], check=True, capture_output=True, timeout=300)
            ok("Servidor MCP de DuckDB listo")
        except Exception as error:
            failure(f"No se ha podido preparar el servidor MCP de DuckDB: {error}")

    from huggingface_hub import get_token

    if get_token():
        ok("Sesión de Hugging Face iniciada")
    else:
        warning("Sin sesión de Hugging Face (opcional, pero recomendable).", "Ejecuta: uv run hf auth login")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="skip every step that needs the network")
    args = parser.parse_args()

    print("Comprobando que todo está listo para el seminario Big Data con IA...")
    check_tools()
    if check_libraries() and not args.offline:
        check_remote_read()
        prepare_demo_data()
        check_model()
        prepare_mcp()

    print("\n" + "=" * 60)
    print(f"Resultado: {results['ok']} correctos, {results['warning']} avisos, {results['failure']} fallos")
    if results["failure"]:
        print("Hay cosas que arreglar: lee los mensajes [FALLO] de arriba.")
        print("Si no lo consigues, consulta 'Problemas frecuentes' en el README.")
    else:
        print("Todo listo para el seminario.")
    print("=" * 60)
    sys.exit(1 if results["failure"] else 0)


if __name__ == "__main__":
    main()
