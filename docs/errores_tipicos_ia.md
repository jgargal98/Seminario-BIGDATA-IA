# Errores típicos de una IA analizando datos

Para la demo y para el apartado «Errores de la IA» del informe del ejercicio.

La columna **Comprobado** indica qué se ha medido sobre los datos reales de la demo (`lukebarousse/data_jobs`) o se ha reproducido al preparar el repositorio. El resto son riesgos habituales: comprobadlos vosotros con Claude y con vuestros datos.

| # | Error | Comprobado | Cómo detectarlo | Arreglo |
|---|---|---|---|---|
| 1 | Cargar el dataset entero en pandas | Medido con `measure_memory.py` | Memoria y tiempo | Regla «usa DuckDB y trae solo resultados» |
| 2 | Buscar habilidades con `LIKE '%sql%'` | Sí: `'%r%'` encuentra 515.746 ofertas y las que piden R son 130.892 | Comparar con la lista convertida (`traps/01`) | Regla + Skill que convierte el texto en lista |
| 3 | Contar una habilidad varias veces por oferta | Sí: 65.385 menciones repetidas | Comparar `count(*)` con `count(DISTINCT ...)` (`traps/02`) | `SELECT DISTINCT row_id, skill` |
| 4 | Dar un salario sin n | Sí: solo el 2,8 % de las ofertas tiene salario anual | Pedir n; `traps/03` | Regla «cada cifra con su n» |
| 5 | Usar `fetchone()` sobre una relación de DuckDB | Sí: desaparece en DuckDB 2.0 | Error de atributo al ejecutar | `connection.sql(query).fetchall()` |
| 6 | Crear la base con una versión de DuckDB distinta a la del servidor MCP | Sí: el servidor exige `duckdb==1.5.6` | El MCP no puede abrir la base | Versión fijada en `pyproject.toml` |
| 7 | Sintaxis de lambda antigua (`x -> ...`) | Riesgo conocido | Aviso de sintaxis obsoleta | `lambda x: ...` |
| 8 | Presentar una columna predicha por un modelo como si fuera un dato | Medido con `classify_text.py` | Comparar con las etiquetas reales | Skill `classify-text`: medir siempre el error |
| 9 | Describir el dataset en vez de la realidad | Sí: el dataset de reseñas tiene exactamente 40.000 reseñas por nivel de estrellas | Mirar la distribución antes de concluir | Skill del dataset con esa trampa |
| 10 | Media dominada por valores extremos | Riesgo conocido | Comparar media y mediana | Regla «mediana + n» |
| 11 | Tratar NULL como 0 o descartarlos sin decirlo | Riesgo conocido | Contar NULL por columna | Regla de nulos; perfilado previo |
| 12 | Concluir causalidad («esta habilidad sube el sueldo») | Riesgo conocido | Leer las conclusiones | Regla «correlación no es causalidad» |
| 13 | Inventar una cifra o una columna que no existe | Riesgo conocido | Cruzar con `results/*.csv` y con `DESCRIBE` | Regla «no inventes»; revisar el informe |
| 14 | Rutas absolutas o aleatoriedad sin semilla | Riesgo conocido | Reproducir en otro equipo | `reproduce.py --check`; `REPEATABLE (42)` |
| 15 | Ignorar el sesgo de selección (solo ofertas con salario) | Riesgo conocido | Comparar perfiles con y sin salario | Mencionarlo en Limitaciones |

## Cómo anotar un error en el informe

Qué propuso la IA, qué evidencia mostró que estaba mal y qué cambio concreto lo evita (regla, Skill o consulta). Un error «arreglado» sin un cambio verificable en el repositorio no cuenta.
