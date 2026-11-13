# Demo de escalado (solo ponentes)

Los alumnos no descargan este dataset: trabajan con el de 205 MB.

## Dataset

[`bagadbilla/amazon-reviews-2023-trimmed`](https://huggingface.co/datasets/bagadbilla/amazon-reviews-2023-trimmed)

- 571.544.897 reseñas en inglés, 34 categorías, 2.018 ficheros Parquet, 85 GB comprimidos.
- Columnas: `rating`, `title`, `text`.
- Es una versión recortada de [Amazon Reviews 2023](https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023) (McAuley Lab, arXiv:2403.03952), que ocupa 750 GB en total. Conviene citar esa fuente.
- Licencia indicada: `other`.

## Tiempos medidos

Consultas remotas con DuckDB, sin sesión de Hugging Face, en un solo equipo y con una sola ejecución. Dependen de la red.

| Consulta | Filas | Tiempo |
|---|---|---|
| `COUNT(*)` en Kindle_Store | 25,6 millones | 8,6 s |
| `COUNT(*)` en todo el dataset | 571,5 millones | 167 s |
| `GROUP BY rating` en Appliances | 2,1 millones | 27 s |
| `GROUP BY rating` en Kindle_Store | 25,6 millones | Sin terminar tras casi 8 min |

Los `COUNT(*)` solo leen los metadatos de cada fichero. El `GROUP BY` tiene que descargar la columna, así que por red no escala: esto también es parte de la explicación.

## Memoria estimada con pandas

Extrapolado de un fichero de Kindle_Store (204.621 filas, 493 bytes por fila). No se ha llegado a cargar el dataset completo.

| Datos | Memoria estimada |
|---|---|
| Kindle_Store | 13 GB |
| Dataset completo | 281 GB |

## Consultas

```sql
-- Fast: reads parquet metadata only
SELECT COUNT(*) FROM 'hf://datasets/bagadbilla/amazon-reviews-2023-trimmed/Kindle_Store/*.parquet';

-- Run before the seminar: takes about 3 minutes
SELECT COUNT(*) FROM 'hf://datasets/bagadbilla/amazon-reviews-2023-trimmed/*/*.parquet';

-- Scans a real column on a mid-size category
SELECT rating, COUNT(*) AS reviews
FROM 'hf://datasets/bagadbilla/amazon-reviews-2023-trimmed/Appliances/*.parquet'
GROUP BY rating
ORDER BY rating;
```
