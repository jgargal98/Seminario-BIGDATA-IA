"""
Turn unstructured text into a column with a Hugging Face model, and measure its error.

Takes a random sample of Spanish product reviews straight from Hugging Face,
predicts the stars from the text alone and compares them with the real stars.
The point: an AI-made column is a prediction, so it must be checked on labelled data.

Usage:
    uv run scripts/classify_text.py
    uv run scripts/classify_text.py --sample 500 --language en
"""

import argparse
import time

import duckdb
import pandas as pd

from common import SENTIMENT_MODEL, TEXT_DATASET, TEXT_DATASET_FILE


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sample", type=int, default=200, help="reviews to classify (CPU: about 10-20 per second)")
    parser.add_argument("--language", default="es", help="de, en, es, fr, ja or zh")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    connection = duckdb.connect()
    connection.sql("INSTALL httpfs; LOAD httpfs;")
    path = f"hf://datasets/{TEXT_DATASET}/{TEXT_DATASET_FILE}"
    # USING SAMPLE runs before WHERE, so the language filter goes in a subquery.
    # The seed makes the demo repeatable: same reviews on every run.
    rows = connection.sql(f"""
        SELECT review_body, stars
        FROM (SELECT review_body, stars FROM '{path}' WHERE language = '{args.language}')
        USING SAMPLE reservoir({args.sample} ROWS) REPEATABLE ({args.seed})
    """).fetchall()
    sample = pd.DataFrame(rows, columns=["review_body", "stars"])
    print(f"Muestra: {len(sample)} reseñas en '{args.language}'")

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
