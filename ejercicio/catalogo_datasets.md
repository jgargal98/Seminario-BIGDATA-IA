# Catálogo de datasets para el ejercicio

Cada alumno usa uno DISTINTO: resérvalo con el profesor. El dataset de la demo (`lukebarousse/data_jobs`) no se puede usar.

Antes de asignarlos, revisad en la ficha de cada dataset la licencia y el número de filas. Los marcados como **comprobado** se han medido durante la preparación del seminario; el resto viene de las fichas públicas.

| Dataset (Hugging Face) | Tipo de datos | Filas | Texto para el modelo | Notas y licencia |
|---|---|---|---|---|
| `srvmishra832/multilingual-amazon-reviews-6-languages` | Reseñas de Amazon en 6 idiomas, con estrellas y categoría | 1.200.000 (**comprobado**) | `review_body` (200.000 en español) | Trampa: exactamente 40.000 reseñas por cada nivel de estrellas y por idioma (equilibrado artificialmente). Copia de un dataset retirado; sin licencia declarada |
| `Yelp/yelp_review_full` | Reseñas con 1-5 estrellas | 650.000 (train) | `text` | Términos de Yelp: uso no comercial |
| `fancyzhx/amazon_polarity` | Reseñas de Amazon, positivas o negativas | 3.600.000 (train) | `title`, `content` | Grande: bueno para el tema de memoria. Apache 2.0 |
| `fancyzhx/dbpedia_14` | Artículos de DBpedia en 14 clases | 560.000 (train) | `content` | Derivado de Wikipedia (CC BY-SA) |
| `fancyzhx/yahoo_answers_topics` | Preguntas y respuestas por tema | 1.400.000 (train) | `question_title`, `best_answer` | Revisar condiciones |
| `stanfordnlp/sentiment140` | Tuits con sentimiento | 1.600.000 | `text` | Datos de redes sociales: no identificar a personas |
| `bagadbilla/amazon-reviews-2023-trimmed` (una categoría) | Reseñas de Amazon 2023 por categoría | Desde 71.000 hasta 67 millones según la categoría (**comprobado**) | `text` | Recorte de Amazon Reviews 2023 (McAuley Lab). Licencia `other`. Elegid una categoría de tamaño medio |

## Criterios para proponer otro dataset

- Al menos 100.000 filas, descarga pública sin registro y licencia que permita analizarlo.
- Al menos una columna de texto libre, para la parte de datos no estructurados.
- Al menos una trampa que obligue a guiar a la IA: nulos, texto con formato, duplicados o sesgos.
- Sin datos personales sensibles.
