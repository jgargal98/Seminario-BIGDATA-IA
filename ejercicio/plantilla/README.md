# TODO: título de tu análisis

TODO: una frase sobre qué pregunta respondes y con qué datos.

## Cómo reproducirlo

Requisitos: Git, uv y Claude Code (ver el README del seminario).

```bash
uv run scripts/download_data.py --dataset TODO/usuario-dataset
```

```bash
uv run scripts/configure_mcp.py
```

```bash
uv run scripts/reproduce.py --check
```

Debe terminar en **REPRODUCIBLE**.

## Contenido

| Fichero | Qué es |
|---|---|
| `question.md` | Pregunta y subpreguntas |
| `CLAUDE.md` | Reglas de trabajo para Claude |
| `.claude/skills/` | Skills del dataset y del método |
| `.mcp.json.example` | Configuración MCP de referencia (el `.mcp.json` real lo genera `configure_mcp.py`) |
| `queries/` | Consultas SQL del análisis |
| `results/` | Resultados y huellas generados por `reproduce.py` |
| `report.md` | Informe final |
