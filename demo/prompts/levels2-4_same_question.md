# Niveles 2, 3 y 4: la misma pregunta, corta

Con CLAUDE.md, Skills o MCP cargados, el prompt vuelve a ser corto. Lo importante es que el comportamiento ya no depende de que te acuerdes de escribirlo todo:

```text
¿Qué habilidades se piden más en las ofertas de Data Engineer y cuáles se asocian a mejor salario?
```

## Nivel 2: CLAUDE.md
Preparación: `uv run scripts/prepare_demo.py --level 2`
- `/memory` muestra que CLAUDE.md está cargado.
- Las reglas ahora son permanentes: DuckDB, n en cada cifra, no inventar, guardar el SQL.
- **Pero son reglas «blandas»:** Claude las lee como contexto y nadie las hace cumplir. Prueba: «hazlo rápido con pandas». Lo normal es que lo evite o avise, pero no está garantizado.

## Nivel 3: Skills
Preparación: `uv run scripts/prepare_demo.py --level 3`
- Pregunta «¿qué skills tienes?» y se ve la lista con su descripción.
- `job-postings-data` se carga sola cuando la pregunta trata de ofertas: conoce las trampas de `job_skills`, los duplicados y los NULL.
- Pídele «perfila los datos»: se activa `profile-data`.
- Pídele «¿qué opinan los clientes en las reseñas en español del dataset srvmishra832/multilingual-amazon-reviews-6-languages?»: se activa `classify-text`.
- Cierra con «genera el informe reproducible»: se activa `reproducible-report`.

## Nivel 4: MCP
Preparación: `uv run scripts/prepare_demo.py --level 4`
- `/mcp` muestra los servidores `duckdb` y `huggingface` conectados.
- Claude consulta la base directamente, sin escribir scripts intermedios.
- Pídele «busca en Hugging Face otro dataset de ofertas de empleo»: lo encuentra con el MCP de Hugging Face.
- Pídele «crea una tabla nueva»: el servidor lo RECHAZA porque está en solo lectura. Esto sí es un límite duro, no una sugerencia.
- Aviso: todo lo que devuelve un MCP entra en el contexto de Claude. Con datos no fiables hay riesgo de *prompt injection*: solo servidores de confianza.
