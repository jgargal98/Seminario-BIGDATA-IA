---
name: duckdb-analysis
description: Método para analizar tablas grandes con DuckDB sin agotar la memoria y con resultados repetibles. Úsala cuando haya que calcular agregados, rankings, medianas o cruces sobre cientos de miles de filas o más.
---

# Análisis con DuckDB sobre datos grandes

## Método
1. Conecta en solo lectura: `duckdb.connect(path, read_only=True)`.
2. Deja que DuckDB agregue y trae a Python solo el RESULTADO (decenas de filas), nunca la tabla.
3. Con Parquet, lee solo las columnas necesarias: `SELECT col1, col2 FROM 'file.parquet'`.
4. Cuenta entidades por su clave (`row_id`). Al expandir listas usa `SELECT DISTINCT` para no contar dos veces la misma oferta.
5. Medianas con `median()` o `quantile_cont()`, SIEMPRE acompañadas de `count(*)`.
6. Descarta grupos pequeños con `HAVING count(*) >= 30`.
7. Guarda cada consulta final en `queries/NN_nombre.sql`: una por fichero, con un comentario de qué responde y `ORDER BY` completo.

## Sintaxis de DuckDB (versión del proyecto: 1.5.6)
- Lista desde texto con comillas simples:
  ```sql
  from_json(replace(job_skills, '''', '"'), '["VARCHAR"]')
  ```
  y después `unnest(...)` para tener una fila por habilidad.
- Lambdas: `list_transform(l, lambda x: x + 1)`. La flecha `x -> ...` está obsoleta.
- Desde Python: `connection.sql(query).fetchall()`. No uses `fetchone()` sobre una relación: desaparece en DuckDB 2.0.

## Antes de dar una cifra
- ¿Sobre cuántas filas (n)? ¿Cuántas eran NULL y se descartaron?
- ¿Son «ofertas» o «menciones»?
- ¿Se puede repetir con el SQL guardado?
