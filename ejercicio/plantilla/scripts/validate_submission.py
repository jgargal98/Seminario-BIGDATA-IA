"""
Check the STRUCTURE of an exercise submission before handing it in.

It does not judge quality (that is what the rubric and the cross review are for);
it catches the mistakes that make a submission incomplete or impossible to reproduce.

Usage:
    uv run scripts/validate_submission.py path/to/your/repository
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

MAX_CLAUDE_MD_LINES = 200
MIN_RULES = 6
MIN_SKILLS = 2
REPORT_SECTIONS = ["resultados", "limitaciones", "errores"]
DATA_SUFFIXES = {".parquet", ".duckdb", ".csv", ".gz", ".zip", ".jsonl"}
TEXT_SUFFIXES = {".md", ".py", ".sql", ".json", ".example", ".toml", ".txt", ".yaml", ".yml"}
# Personal folders in Windows, macOS and Linux.
ABSOLUTE_PATH = re.compile(r"([A-Za-z]:[\\/]+Users[\\/]|/Users/|/home/)")

results = {"ok": 0, "warning": 0, "failure": 0}


def report(kind, label, text):
    results[kind] += 1
    print(f"  [{label}] {text}")


def ok(text):
    report("ok", " OK  ", text)


def warning(text):
    report("warning", "AVISO", text)


def failure(text):
    report("failure", "FALLO", text)


def tracked_files(repo):
    """Files that would be submitted: git-tracked if possible, otherwise everything."""
    try:
        output = subprocess.run(["git", "-C", str(repo), "ls-files"], capture_output=True, text=True, check=True).stdout
        files = [repo / line for line in output.splitlines() if line]
        if files:
            return files, True
    except Exception:
        pass
    ignored = {".git", ".venv", "data", "__pycache__", ".cache"}
    return [p for p in repo.rglob("*") if p.is_file() and not ignored & set(p.relative_to(repo).parts)], False


def has_placeholder(text):
    return "TODO" in text


def check_question(repo):
    path = repo / "question.md"
    if not path.exists():
        failure("Falta question.md")
    elif has_placeholder(path.read_text(encoding="utf-8")):
        failure("question.md todavía tiene TODO de la plantilla")
    else:
        ok("question.md")


def check_claude_md(repo):
    path = repo / "CLAUDE.md"
    if not path.exists():
        failure("Falta CLAUDE.md")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    rules = [line for line in lines if re.match(r"^\s*\d+\.\s+\S", line)]
    if len(lines) > MAX_CLAUDE_MD_LINES:
        failure(f"CLAUDE.md tiene {len(lines)} líneas (máximo {MAX_CLAUDE_MD_LINES})")
    elif len(rules) < MIN_RULES:
        failure(f"CLAUDE.md tiene {len(rules)} reglas numeradas (mínimo {MIN_RULES})")
    elif has_placeholder("\n".join(lines)):
        failure("CLAUDE.md todavía tiene TODO de la plantilla")
    else:
        ok(f"CLAUDE.md: {len(rules)} reglas, {len(lines)} líneas")


def check_skills(repo):
    skills = sorted((repo / ".claude" / "skills").glob("*/SKILL.md"))
    valid = 0
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        name = skill.parent.name
        frontmatter = re.match(r"^---\s*\n(.*?)\n---", text, flags=re.S)
        if not frontmatter or "name:" not in frontmatter.group(1) or "description:" not in frontmatter.group(1):
            failure(f"Skill {name}: falta la cabecera con name y description")
        elif has_placeholder(text):
            failure(f"Skill {name}: todavía tiene TODO de la plantilla")
        else:
            valid += 1
            ok(f"Skill {name}")
    if valid < MIN_SKILLS:
        failure(f"Hay {valid} Skills válidas (mínimo {MIN_SKILLS})")


def check_mcp(repo, files, uses_git):
    example = repo / ".mcp.json.example"
    if not example.exists():
        failure("Falta .mcp.json.example")
    else:
        try:
            servers = json.loads(example.read_text(encoding="utf-8"))["mcpServers"]
            args = servers["duckdb"].get("args", [])
            if "--read-write" in args:
                failure(".mcp.json.example abre DuckDB en lectura y escritura: debe ser solo lectura")
            else:
                ok(".mcp.json.example con DuckDB en solo lectura")
        except Exception as error:
            failure(f".mcp.json.example no es válido (se espera un servidor 'duckdb'): {error}")
    if any(f.name == ".mcp.json" for f in files):
        failure(".mcp.json está en el repositorio: tiene rutas de tu ordenador, añádelo a .gitignore")
    elif not uses_git:
        warning("No es un repositorio de Git: no se puede comprobar qué ficheros se van a subir")


def check_queries(repo):
    queries = sorted((repo / "queries").glob("*.sql"))
    if not queries:
        failure("No hay consultas en queries/*.sql")
        return
    unordered = [q.name for q in queries if "order by" not in q.read_text(encoding="utf-8").lower()]
    if unordered:
        failure(f"Consultas sin ORDER BY (el orden de las filas puede cambiar): {', '.join(unordered)}")
    else:
        ok(f"{len(queries)} consultas en queries/, todas con ORDER BY")
    if (repo / "results" / "fingerprints.json").exists():
        ok("results/fingerprints.json presente")
    else:
        failure("Falta results/fingerprints.json: ejecuta uv run scripts/reproduce.py")


def check_report(repo):
    path = repo / "report.md"
    if not path.exists():
        failure("Falta report.md")
        return
    text = path.read_text(encoding="utf-8")
    headings = " ".join(line.lower() for line in text.splitlines() if line.startswith("#"))
    missing = [s for s in REPORT_SECTIONS if s not in headings]
    if missing:
        failure(f"A report.md le faltan secciones: {', '.join(missing)}")
    elif has_placeholder(text):
        failure("report.md todavía tiene TODO de la plantilla")
    else:
        ok("report.md con resultados, limitaciones y errores de la IA")


def check_privacy(repo, files):
    data = [f for f in files if f.suffix.lower() in DATA_SUFFIXES and "results" not in f.relative_to(repo).parts]
    if data:
        failure(f"Hay ficheros de datos en el repositorio: {', '.join(f.name for f in data[:5])}")
    else:
        ok("Sin ficheros de datos en el repositorio")

    with_paths = []
    for path in files:
        if path.suffix.lower() in TEXT_SUFFIXES and path.name != ".gitignore":
            try:
                if ABSOLUTE_PATH.search(path.read_text(encoding="utf-8", errors="ignore")):
                    with_paths.append(path.relative_to(repo).as_posix())
            except OSError:
                pass
    if with_paths:
        failure(f"Rutas personales de tu ordenador en: {', '.join(with_paths[:5])}")
    else:
        ok("Sin rutas personales")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo", nargs="?", default=".")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        sys.exit(f"No existe la carpeta {repo}")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print(f"Validando la entrega en {repo}\n")
    files, uses_git = tracked_files(repo)
    check_question(repo)
    check_claude_md(repo)
    check_skills(repo)
    check_mcp(repo, files, uses_git)
    check_queries(repo)
    check_report(repo)
    check_privacy(repo, files)

    print(f"\nResultado: {results['ok']} correctos, {results['warning']} avisos, {results['failure']} fallos")
    print("Estructura completa." if not results["failure"] else "La entrega no está completa: corrige los [FALLO].")
    sys.exit(1 if results["failure"] else 0)


if __name__ == "__main__":
    main()
