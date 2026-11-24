"""Shared paths and settings for every script in the seminar repository."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PARQUET_PATH = DATA_DIR / "jobs.parquet"
DATABASE_PATH = DATA_DIR / "analysis.duckdb"
TABLE = "jobs"

DEMO_DATASET = "lukebarousse/data_jobs"
TEXT_DATASET = "srvmishra832/multilingual-amazon-reviews-6-languages"
TEXT_DATASET_FILE = "data/train-00000-of-00001.parquet"
SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"

# A small labelled sample of reviews, saved once by check_setup.py so the text demo
# does not depend on the classroom network. The seed keeps it identical on every machine.
REVIEWS_SAMPLE_PATH = DATA_DIR / "reviews_es.parquet"
REVIEWS_SAMPLE_SIZE = 100
REVIEWS_SAMPLE_LANGUAGE = "es"
REVIEWS_SAMPLE_SEED = 42

# Pinned so every student runs the same server, which in turn pins duckdb==1.5.6.
DUCKDB_MCP_SERVER = "mcp-server-motherduck@1.1.0"
# Without it uvx picks the newest Python, which may have no duckdb 1.5.6 wheels yet.
DUCKDB_MCP_UVX_ARGS = ["--python", "3.12", DUCKDB_MCP_SERVER]
HUGGINGFACE_MCP_URL = "https://huggingface.co/mcp"

# Symlinks need special permissions on Windows; Hugging Face warns about it
# even though it works fine without them.
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")

# Legacy Windows consoles default to a code page that breaks on accented text.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def format_int(number):
    """Spanish thousands separator, e.g. 785.741."""
    return f"{number:,}".replace(",", ".")


def mcp_config(database_path, max_rows=200):
    """MCP servers used from level 4 on. DuckDB opens the file read-only by default."""
    return {
        "mcpServers": {
            "duckdb": {
                "type": "stdio",
                "command": "uvx",
                "args": [
                    *DUCKDB_MCP_UVX_ARGS,
                    "--db-path",
                    Path(database_path).resolve().as_posix(),
                    "--max-rows",
                    str(max_rows),
                ],
            },
            "huggingface": {"type": "http", "url": HUGGINGFACE_MCP_URL},
        }
    }
