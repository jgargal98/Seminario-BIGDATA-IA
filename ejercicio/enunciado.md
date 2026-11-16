# Ejercicio: construye tu analista de Big Data con IA

## Objetivo

Construir con Claude Code un sistema que analice un dataset de cientos de miles de registros de forma fiable: sin inventar resultados, respetando los límites de los datos y de modo que otra persona pueda repetirlo.

No se trata de que la IA dé una respuesta bonita, sino de que **el sistema funcione y otro pueda comprobarlo**.

## Qué tienes que entregar

Un repositorio de GitHub, partiendo de la carpeta [plantilla/](plantilla/), con:

1. **`question.md`:** una pregunta de investigación propia y al menos 4 subpreguntas que la respondan.
2. **`CLAUDE.md`:** al menos 6 reglas, cada una ligada a un fallo real que observaste en Claude. Máximo 200 líneas.
3. **Al menos 2 Skills** en `.claude/skills/<nombre>/SKILL.md`:
   - una **del dataset**: columnas, significado, calidad, trampas y limitaciones que descubras explorándolo;
   - una **de método**: cómo hacer bien un tipo de análisis (comparar grupos, detectar valores atípicos, clasificar texto...).
4. **MCP:** `.mcp.json.example` con el servidor de DuckDB en solo lectura, más el script que genera tu `.mcp.json` local.
5. **Datos no estructurados:** al menos una columna creada con un modelo de Hugging Face a partir de texto, sobre una muestra justificada y con su error medido (ver `scripts/classify_text.py` del seminario).
6. **`queries/` y `scripts/`:** el análisis completo, repetible con `uv run scripts/reproduce.py --check`.
7. **`report.md`:** resultados con n en cada cifra, limitaciones honestas y un **registro de errores de la IA**: al menos 3, cada uno con qué hizo mal, cómo lo detectaste y qué cambiaste en CLAUDE.md, en una Skill o en una consulta para que no vuelva a pasar.

## Reglas

- Elige el dataset que quieras del [catálogo](catalogo_datasets.md). El dataset de la demo no vale.
- No subas los datos (se descargan con tu script), ni claves, ni rutas de tu ordenador.
- Antes de entregar, `uv run scripts/validate_submission.py .` (desde tu repositorio) tiene que terminar sin errores.

## Consejos

- Trabaja con **muestras pequeñas** mientras construyes el sistema, para no agotar la cuota de tu plan Pro.
- Un error de la IA que no aparece en tu informe no cuenta a tu favor. Si la IA nunca se equivocó, no la has puesto a prueba lo suficiente: busca trampas (nulos, duplicados, tipos, tamaño, sesgos).

## Evaluación

Se valora sobre todo que el sistema funcione y se pueda comprobar: reglas y Skills basadas en errores reales de la IA, cifras acompañadas de su n, errores del modelo medidos y un análisis que otra persona pueda repetir.
