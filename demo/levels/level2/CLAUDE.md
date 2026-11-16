# Proyecto: análisis de ofertas de empleo del sector datos

## Contexto
- Datos: `../../data/analysis.duckdb`, tabla `jobs` (785.741 filas, una por oferta).
  Los mismos datos están en `../../data/jobs.parquet`.
- Columnas clave: `row_id` (identificador único), `job_title_short`, `job_country`,
  `salary_year_avg` (solo el 2,8 % tiene valor), `job_skills` (TEXTO con forma de lista, no una lista real).
- El entorno de Python es el del proyecto: ejecuta siempre con `uv run python ...` o `uv run ../../scripts/<script>.py`.
  No instales paquetes.

## Reglas de trabajo (síguelas siempre)
1. Usa DuckDB (SQL). No cargues el dataset completo en pandas: trae a Python solo resultados.
2. Abre la base en solo lectura. Nunca modifiques ni borres los datos de origen.
3. Con CADA cifra que des, indica sobre cuántas ofertas (n) está calculada.
4. Distingue «ofertas» de «menciones»: una habilidad cuenta una vez por oferta.
5. Los NULL no son ceros: di cuántos hay y cómo los has tratado.
6. No inventes resultados. Si no has podido comprobar algo, dilo explícitamente.
7. No uses `LIKE '%texto%'` para buscar habilidades (`'%sql%'` también encuentra nosql o mysql). Convierte el texto en lista.
8. Guarda cada consulta final en `queries/` (numerada, con `ORDER BY` completo) para que sea repetible.
9. Con grupos pequeños (n < 30) no saques conclusiones: márcalos como poco fiables.

## Formato de respuesta
- Primero la respuesta en 2-3 líneas; después las tablas; después las limitaciones.
- Termina siempre con «Qué no sé / qué conviene verificar».

## Herramientas del proyecto
- `uv run ../../scripts/demo/profile_dataset.py` perfila la tabla.
- `uv run ../../scripts/demo/reproduce.py` repite todas las consultas de `queries/` y guarda sus huellas.
