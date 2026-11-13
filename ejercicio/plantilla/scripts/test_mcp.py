"""
Test the DuckDB MCP server WITHOUT Claude: list tools, run a query, try to write.

Usage:
    uv run scripts/test_mcp.py --config demo/session/.mcp.json
"""

import argparse
import asyncio
import json
import os
import shutil
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from common import TABLE


def text_of(result):
    return " ".join(getattr(c, "text", str(c)) for c in result.content)


def is_rejected(result):
    text = text_of(result).lower()
    return bool(getattr(result, "isError", False)) or "read-only" in text or '"success": false' in text


async def run(config_path):
    server = json.loads(config_path.read_text(encoding="utf-8"))["mcpServers"]["duckdb"]
    # On Windows a bare "uvx" is not always resolved by the subprocess layer.
    command = shutil.which(server["command"]) or server["command"]
    # The MCP client passes only a minimal environment by default; uv needs the
    # full one to find its cache and installed Pythons, as Claude Code does.
    params = StdioServerParameters(command=command, args=server.get("args", []), env=dict(os.environ))
    failures = 0
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [t.name for t in (await session.list_tools()).tools]
            print(f"[ OK  ] Servidor arrancado. Herramientas: {', '.join(tools)}")

            result = await session.call_tool("execute_query", {"sql": f"SELECT count(*) AS rows FROM {TABLE}"})
            if is_rejected(result):
                print(f"[FALLO] La consulta de lectura falla: {text_of(result)[:200]}")
                failures += 1
            else:
                print(f"[ OK  ] Consulta de lectura: {' '.join(text_of(result).split())[:160]}")

            result = await session.call_tool("execute_query", {"sql": "CREATE TABLE write_test (x INT)"})
            if is_rejected(result):
                print("[ OK  ] Escritura rechazada: el servidor está en solo lectura")
            else:
                print(f"[FALLO] Se ha permitido escribir: {text_of(result)[:200]}")
                failures += 1
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default=".mcp.json")
    args = parser.parse_args()
    sys.exit(1 if asyncio.run(run(Path(args.config))) else 0)


if __name__ == "__main__":
    main()
