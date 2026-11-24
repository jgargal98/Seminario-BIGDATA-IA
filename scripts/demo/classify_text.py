"""
Turn unstructured text into a column with a Hugging Face model, and measure its error.

Predicts the stars of Spanish product reviews from the text alone and compares them
with the real stars. The point: an AI-made column is a prediction, so it must be
checked on labelled data.

By default it uses the sample of reviews that check_setup.py saved in data/, so the
demo does not depend on the network. With --sample or --language it reads a new
sample straight from Hugging Face instead (slower: it goes through the remote file).

Usage:
    uv run scripts/demo/classify_text.py
    uv run scripts/demo/classify_text.py --sample 500 --language en
"""

import argparse
import sys
import time
from pathlib import Path

import duckdb
import pandas as pd

# Shared settings live one folder up, in scripts/common.py and scripts/install/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "install"))

from common import (
    REVIEWS_SAMPLE_LANGUAGE,
    REVIEWS_SAMPLE_PATH,
    REVIEWS_SAMPLE_SEED,
    REVIEWS_SAMPLE_SIZE,
    ROOT,
    SENTIMENT_MODEL,
)
from download_data import remote_reviews_query


def load_sample(connection, args):
    """Return (DataFrame, where it came from): the saved sample, or a fresh remote one."""
    remote = args.sample is not None or args.language != REVIEWS_SAMPLE_LANGUAGE
    if not remote and REVIEWS_SAMPLE_PATH.exists():
        rows = connection.sql(f"SELECT review_body, stars FROM '{REVIEWS_SAMPLE_PATH.as_posix()}'").fetchall()
        return pd.DataFrame(rows, columns=["review_body", "stars"]), REVIEWS_SAMPLE_PATH.relative_to(ROOT).as_posix()

    size = args.sample or REVIEWS_SAMPLE_SIZE
    print(f"Leyendo {size} reseñas de Hugging Face (puede tardar unos minutos)...", flush=True)
    connection.sql("INSTALL httpfs; LOAD httpfs;")
    rows = connection.sql(remote_reviews_query(size, args.language, args.seed)).fetchall()
    return pd.DataFrame(rows, columns=["review_body", "stars"]), "Hugging Face"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sample", type=int, help="read a new sample of this size from Hugging Face")
    parser.add_argument("--language", default=REVIEWS_SAMPLE_LANGUAGE, help="de, en, es, fr, ja or zh")
    parser.add_argument("--seed", type=int, default=REVIEWS_SAMPLE_SEED)
    args = parser.parse_args()

    connection = duckdb.connect()
    sample, source = load_sample(connection, args)
    print(f"Muestra: {len(sample)} reseñas en '{args.language}' ({source})")

    print("Cargando el modelo...", flush=True)
    from transformers import pipeline

    classifier = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
    start = time.time()
    predictions = classifier(sample["review_body"].tolist(), truncation=True, batch_size=16)
    sample["predicted"] = [int(p["label"].split()[0]) for p in predictions]
    print(f"Clasificadas en {time.time() - start:.1f} s\n")

    hits = (sample["predicted"] == sample["stars"]).mean()
    close = ((sample["predicted"] - sample["stars"]).abs() <= 1).mean()
    print(f"Aciertos exactos: {hits:.0%}   A una estrella o menos: {close:.0%}\n")

    # DuckDB can query the pandas DataFrame directly by its variable name.
    print(connection.sql("""
        SELECT stars AS estrellas_reales,
               count(*) AS resenas,
               round(avg(predicted), 2) AS media_predicha
        FROM sample GROUP BY 1 ORDER BY 1
    """))


if __name__ == "__main__":
    main()
