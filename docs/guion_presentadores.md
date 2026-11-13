# Guion de presentadores (unos 105 minutos)

Reparto: **A** y **B** se alternan por bloques; quien no habla maneja el portátil.
Idea que debe quedar: **la IA analiza bien cuando tú la guías bien, y solo sabes si lo hizo bien si lo verificas.**

Abrid `claude` siempre dentro de `demo/session`, nunca en la raíz del repositorio: en la raíz, Claude ve también las Skills de la plantilla del ejercicio.

## Antes del día

- [ ] Todos los alumnos ejecutan `uv run scripts/check_setup.py` ([requisitos](requisitos_alumnos.md)).
- [ ] **Ensayo completo con Claude Code**, nivel a nivel. Claude no es determinista: apuntad lo que hace de verdad y haced capturas de respaldo.
- [ ] `uv run scripts/prepare_demo.py --level 4` y después `uv run scripts/test_mcp.py --config demo/session/.mcp.json` hasta que salga todo en OK.
- [ ] Lanzad el `COUNT(*)` del dataset grande de [demo-escalado.md](demo-escalado.md) antes de empezar: tarda unos 3 minutos.
- [ ] Plan B sin red: `uv run scripts/make_synthetic.py` y `uv run scripts/download_data.py --synthetic` (avisar a la clase de que son datos inventados).
- [ ] No gastéis la cuota del plan Pro antes del seminario.
- [ ] Rellenad el título real del seminario de MCP en la diapositiva del nivel 4.

## Mapa

| Min | Bloque | Quién | Big Data que aparece | IA |
|---|---|---|---|---|
| 0-5 | Arranque | A | | Demo del nivel 4 funcionando; la escalera |
| 5-21 | Big Data | B | 5 V, ciclo de vida, escalado, Parquet, datos no estructurados | Modelo de Hugging Face en directo |
| 21-41 | Nivel 1: prompt | A | Memoria, escalado, red como cuello de botella | Prompt sin contexto y prompt estructurado |
| 41-56 | Nivel 2: CLAUDE.md | B | Calidad de datos | Reglas permanentes y «blandas» |
| 56-81 | Nivel 3: Skills | A | Datos semiestructurados y no estructurados | Conocimiento bajo demanda |
| 81-91 | Nivel 4: MCP | B | Big Data como ecosistema | Herramientas conectadas, solo lectura |
| 91-101 | Cierre y ejercicio | A+B | | |
| 101-106 | Preguntas | A+B | | |

## 0-5 · Arranque (A)

- Enseñad el final primero: con el nivel 4 preparado, una pregunta corta y Claude respondiendo con n, consultas guardadas y limitaciones.
- Tres criterios en la pizarra: **sin inventar · respetando los límites de los datos · repetible por otra persona**.
- La escalera, visible durante todo el seminario: **prompt → CLAUDE.md → Skills → MCP**. Cada nivel resuelve algo que el anterior no puede.

## 5-21 · Big Data (B)

Ver [teoria_bigdata.md](teoria_bigdata.md). Todo con el dataset de la demo abierto en pantalla.

1. **Las 5 V** (4 min) con los datos reales: 785.741 ofertas (volumen), texto, números y listas dentro de texto (variedad), el 97,2 % sin salario (veracidad)...
2. **Ciclo de vida** (2 min): ingesta → almacenamiento → procesamiento → análisis → comunicación.
3. **Escalado** (4 min): vertical frente a horizontal, Hadoop y MapReduce, Spark. La pregunta queda abierta: «¿hace falta un clúster para esto?».
4. **Formatos** (3 min): el mismo dataset ocupa 231 MB en CSV y 39 MB en Parquet. Por qué.
5. **Datos no estructurados** (3 min): `uv run scripts/classify_text.py`. 200 reseñas en español clasificadas en unos 15 s. El modelo acierta la estrella exacta el 46 % de las veces y se queda a una estrella o menos el 90 %. **Una columna creada por IA es una predicción con error**, y hay que medirlo.

## 21-41 · Nivel 1: el prompt (A)

Preparación: `uv run scripts/prepare_demo.py --level 1`. Prompts en [level1_prompts.md](../demo/prompts/level1_prompts.md).

1. **Prompt sin contexto** (6 min). Mientras trabaja, apuntad en la pizarra cada fallo: pandas, `LIKE`, duplicados, n... Si acierta, decidlo.
2. **Escalado, ahora con números** (6 min), en el momento en que Claude carga los datos:
   - `uv run scripts/measure_memory.py`: pandas con el CSV entero usa 751 MB; DuckDB sobre Parquet, 44 MB y 0,3 s.
   - Este dataset cabe en un portátil. El de [demo-escalado.md](demo-escalado.md) no: 571 millones de reseñas, unos 281 GB en pandas. DuckDB cuenta una categoría de 25,6 millones en 9 s porque solo lee metadatos, pero agrupar esa categoría por red no termina en 8 minutos. **La red pasa a ser el cuello de botella**, y por eso existen los clústeres con los datos y el cálculo juntos.
   - Las trampas: `demo/queries/traps/`. `LIKE '%r%'` da 515.746 ofertas; las que piden R son 130.892.
3. **Prompt estructurado** (5 min): contexto, tarea, restricciones y formato, con modo plan (`Shift+Tab`). Comparad con la pizarra.
4. **Por qué no basta** (3 min): la tabla del final de los prompts, que anuncia los tres niveles siguientes.

## 41-56 · Nivel 2: CLAUDE.md (B)

Preparación: `uv run scripts/prepare_demo.py --level 2`. Ver [levels2-4_same_question.md](../demo/prompts/levels2-4_same_question.md).

- Qué es: instrucciones que Claude lee al empezar cada sesión y que se versionan con el proyecto. Corto (menos de 200 líneas) y concreto.
- Enseñad `demo/levels/level2/CLAUDE.md`: **cada regla responde a un fallo de la pizarra**. Las reglas de nulos, n y menciones son la teoría de calidad de datos.
- La pregunta corta, `/memory` y comparación con el nivel 1.
- Honestidad: son reglas **blandas**. «Hazlo rápido con pandas»: puede saltárselas.

## 56-81 · Nivel 3: Skills (A)

Preparación: `uv run scripts/prepare_demo.py --level 3`.

- Qué resuelven: CLAUDE.md siempre está cargado y no puede contenerlo todo. Una Skill es una carpeta con un `SKILL.md` que Claude carga **solo cuando la tarea lo pide**, decidiendo por la `description`.
- Las 5 Skills: `profile-data`, `duckdb-analysis`, `job-postings-data`, `classify-text`, `reproducible-report`.
- En directo: «perfila los datos» → la pregunta → la pregunta sobre reseñas (`classify-text`) → «genera el informe reproducible». Preguntad qué Skill ha usado en cada paso.
- La `description` lo es todo: si está mal escrita, la Skill no se usa nunca.
- **DAAF** como ejemplo real: la misma idea con decenas de Skills y agentes para investigación con datos.
- Reproducibilidad: `uv run ../../scripts/reproduce.py` y después `--check`. «Esto es lo que hará vuestro compañero con vuestro repositorio.»

## 81-91 · Nivel 4: MCP (B)

Preparación: `uv run scripts/prepare_demo.py --level 4`. MCP ya se ha explicado en el seminario de los compañeros: aquí solo lo que aporta a Big Data.

- `/mcp`: servidores `duckdb` y `huggingface` conectados.
- La pregunta: ahora Claude consulta la base directamente.
- «Busca en Hugging Face otro dataset de ofertas de empleo»: Big Data como ecosistema de fuentes y herramientas.
- «Crea una tabla nueva»: rechazado. **Solo lectura es un límite duro**, no una sugerencia.
- Seguridad: lo que devuelve un MCP entra en el contexto de Claude. Solo servidores de confianza.

## 91-101 · Cierre y ejercicio (A+B)

- La escalera completa: prompt (sugerencia) → CLAUDE.md (contexto permanente) → Skill (saber bajo demanda) → MCP en solo lectura (límite técnico).
- Volver al nivel 1: lo que antes eran instrucciones largas ahora es una frase, pero **revisar el resultado sigue siendo cosa vuestra**.
- El ejercicio: [enunciado](../ejercicio/enunciado.md), [rúbrica](../ejercicio/rubrica.md), [revisión cruzada](../ejercicio/revision_cruzada.md), [catálogo](../ejercicio/catalogo_datasets.md) y [plantilla](../ejercicio/plantilla/). Reparto de datasets.

## Si algo falla en directo

| Fallo | Qué hacer |
|---|---|
| Claude tarda o se queda sin cuota | Capturas de respaldo y explicar qué habría pasado |
| Claude acierta todo en el nivel 1 | Decirlo y enseñar `demo/queries/traps/` |
| El MCP no conecta | `uv run scripts/test_mcp.py --config demo/session/.mcp.json` |
| Sin red | Plan B con datos sintéticos, avisando |

## Preguntas probables

- **¿Por qué DuckDB y no Spark?** A este tamaño sobra un portátil. Spark compensa cuando los datos no caben en una máquina o hay que procesarlos de forma continua.
- **¿Es seguro dar mis datos a una IA?** Depende de los datos y del plan. Con datos personales o sensibles, no. Con datos públicos como estos, sí.
- **¿Claude cumple siempre el CLAUDE.md?** No siempre: es contexto. Lo imprescindible se garantiza con permisos o con herramientas en solo lectura.
- **¿Y si la IA se equivoca igual con la Skill?** Por eso el informe pide los errores detectados y existe la revisión cruzada.
