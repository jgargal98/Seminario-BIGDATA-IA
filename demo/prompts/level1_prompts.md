# Nivel 1: el prompt

Prepara la sesión con `uv run scripts/prepare_demo.py --level 1`, entra en `demo/session` y abre `claude`.
Se lanzan dos prompts seguidos, cada uno en una sesión nueva de Claude.

## 1a. Prompt sin contexto

Pégalo tal cual:

```text
Analiza ../../data/jobs.parquet y dime qué habilidades se piden más para Data Engineer y cuáles pagan mejor.
```

### Qué observar (en voz alta y apuntado en la pizarra)
- ¿Carga TODO con pandas? Momento para explicar escalado y memoria (`uv run scripts/measure_memory.py`).
- ¿Cómo trata `job_skills`? Es TEXTO con forma de lista, no una lista real.
- ¿Usa `LIKE '%sql%'`? Entonces cuenta también nosql, mysql y postgresql.
- ¿Cuenta ofertas o menciones? ¿Quita las habilidades repetidas dentro de una oferta?
- ¿Da el salario sin decir cuántas ofertas lo tienen? Solo el 2,8 % tiene salario.
- ¿Dice cuántas filas usó (n)? ¿Guarda el código para repetirlo?

Si Claude acierta en todo, se dice sin disimular: «hoy ha acertado; ¿cómo lo garantizamos mañana, con otro dataset y otra persona?».
Las consultas de `demo/queries/traps/` enseñan cuánto cambia el resultado con el enfoque ingenuo.

## 1b. Prompt estructurado: contexto, tarea, restricciones, formato

```text
CONTEXTO
- Datos: ../../data/jobs.parquet (ofertas de empleo del sector datos, 785.741 filas).
- Columnas relevantes: row_id, job_title_short, job_skills (texto con forma de lista,
  por ejemplo "['python', 'sql']"), salary_year_avg (casi siempre NULL), job_country.
- Es un dataset grande: no lo cargues entero en pandas; usa DuckDB.
- Ejecuta Python con: uv run python

TAREA
¿Qué habilidades se piden más en las ofertas de 'Data Engineer' y cuáles se
asocian a mejor salario?

RESTRICCIONES
- Cuenta cada habilidad UNA vez por oferta.
- Ignora las ofertas sin habilidades; para salarios, ignora las que no tienen salario.
- Con cada cifra, indica sobre cuántas ofertas (n) está calculada.
- Si no estás seguro de algo, dilo en vez de suponerlo.

FORMATO
- Tabla con las 15 habilidades más pedidas (ofertas y % del total).
- Tabla de salario mediano por habilidad (solo habilidades con n >= 30).
- Guarda el SQL en queries/ para poder repetirlo.
```

Antes de ejecutarlo, conviene pulsar `Shift+Tab` para entrar en **modo plan**: Claude propone un plan y no ejecuta nada hasta que se aprueba.

### Por qué un buen prompt no basta
| Limitación | La resuelve |
|---|---|
| Hay que reescribirlo cada vez, y cada persona lo escribe distinto | CLAUDE.md (nivel 2) |
| Por bueno que sea, no conoce las trampas de tus datos | Skills (nivel 3) |
| No puede consultar ni buscar datos con herramientas que no tiene | MCP (nivel 4) |
