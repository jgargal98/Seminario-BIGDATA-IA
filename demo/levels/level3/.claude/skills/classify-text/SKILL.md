---
name: classify-text
description: Convierte texto libre (reseñas, comentarios, descripciones) en una columna con un modelo de Hugging Face y mide su error. Úsala cuando haya que clasificar, puntuar o etiquetar texto no estructurado que SQL no puede analizar.
---

# Clasificar texto con un modelo de Hugging Face

## Reparto del trabajo
- Tú (Claude) escribes y ejecutas el código. **No clasifiques los textos leyéndolos tú**: no escala y gasta la cuota.
- Un modelo pequeño de Hugging Face hace el trabajo masivo en el ordenador del usuario.
- DuckDB elige la muestra y analiza el resultado con SQL.

## Método
1. Elige una **muestra aleatoria con semilla** con DuckDB:
   `USING SAMPLE reservoir(500 ROWS) REPEATABLE (42)`.
   Cuidado: `USING SAMPLE` se aplica ANTES del `WHERE`. Para muestrear un subconjunto, filtra en una subconsulta:
   `SELECT * FROM (SELECT ... WHERE language = 'es') USING SAMPLE reservoir(500 ROWS) REPEATABLE (42)`.
2. Clasifica con `transformers.pipeline(..., truncation=True, batch_size=16)`.
   Modelo por defecto para reseñas en varios idiomas: `nlptown/bert-base-multilingual-uncased-sentiment` (de 1 a 5 estrellas).
3. **Mide el error** si hay una etiqueta real (por ejemplo, las estrellas): % de aciertos exactos y % a una estrella o menos.
   Sin esa comparación, la columna predicha no se puede presentar como dato.
4. Analiza la columna nueva con SQL: DuckDB consulta un DataFrame de pandas por su nombre de variable.

## Ejemplo funcionando
`uv run --project "<repositorio>" "<repositorio>/scripts/demo/classify_text.py"` clasifica la muestra de 100 reseñas en español que `check_setup.py` guardó en la carpeta `data/` del repositorio (no necesita red).
Con `--sample N --language xx` saca una muestra nueva directamente de Hugging Face; es más lento porque recorre el fichero remoto.

## Al informar
- Di siempre que es una **predicción**, cuántos textos se clasificaron y el error medido.
- Una muestra pequeña no permite conclusiones sobre grupos pequeños.
