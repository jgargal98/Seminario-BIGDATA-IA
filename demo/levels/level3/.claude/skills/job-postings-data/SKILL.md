---
name: job-postings-data
description: Conocimiento del dataset de ofertas de empleo de datos (lukebarousse/data_jobs, tabla jobs): columnas, trampas de job_skills, salarios casi siempre vacíos y sesgos. Úsala cuando la pregunta trate de habilidades, salarios, puestos, empresas o países de las ofertas.
---

# Dataset de ofertas de empleo (data_jobs)

Una fila = una oferta de 2023. Tabla `jobs`, clave `row_id`. Origen: Hugging Face `lukebarousse/data_jobs`, licencia Apache 2.0.

## Cifras de referencia (comprobadas sobre los datos reales)
| Dato | Valor |
|---|---|
| Ofertas | 785.741 |
| Ofertas de Data Engineer | 186.241 |
| Con `salary_year_avg` | 22.003 (2,8 %) |
| Con `job_skills` | 668.704 |

Si un cálculo tuyo contradice esta tabla, revisa el cálculo antes de seguir.

## Columnas útiles
- `job_title_short`: puesto normalizado (Data Engineer, Data Scientist, Data Analyst...).
- `job_country`, `job_location`: ubicación.
- `salary_year_avg`: salario anual en dólares. **Casi siempre NULL**: muestra siempre n.
- `salary_hour_avg`: salario por hora; no lo mezcles con el anual.
- `job_skills`: **TEXTO** con aspecto de lista de Python, por ejemplo `['python', 'sql']`.

## Trampas conocidas
1. `job_skills` no es una lista: hay que convertirla (ver la skill `duckdb-analysis`).
2. `LIKE '%sql%'` cuenta nosql, mysql, postgresql... En estos datos infla `sql` un 5 %.
   `LIKE '%r%'` encuentra 515.746 ofertas cuando las que piden R son 130.892.
3. Hay habilidades repetidas dentro de la misma oferta (65.385 menciones de más):
   usa `DISTINCT` por (oferta, habilidad).
4. El salario medio engaña por los valores extremos: usa la **mediana**.
5. Las ofertas con salario no son una muestra aleatoria (sesgo hacia ciertos países y portales).
   Debe aparecer como limitación en cualquier conclusión sobre salarios.
6. Correlación no es causalidad: «las ofertas con X pagan más» no significa «aprender X sube el sueldo».

## Consultas de referencia
`../../demo/queries/01_top_skills.sql` y `../../demo/queries/02_salary_by_skill.sql`.
