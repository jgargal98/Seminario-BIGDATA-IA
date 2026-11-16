# Fundamentos de Big Data

Las cifras están medidas sobre los datos reales de la demo.

## 1. Qué es Big Data y las 5 V

Gartner define Big Data como «activos de información de gran volumen, alta velocidad y/o gran variedad que requieren formas de procesamiento rentables e innovadoras para mejorar la comprensión, la toma de decisiones y la automatización de procesos». La definición parte de las tres dimensiones propuestas por Laney (2001), a las que después se añadieron veracidad y valor.

| V | Significado | En el dataset de la demo |
|---|---|---|
| Volumen | Cantidad de datos | 785.741 ofertas; 571 millones de reseñas en Amazon Reviews 2023 |
| Velocidad | Ritmo al que llegan y hay que procesarlos | Ofertas nuevas cada día |
| Variedad | Tipos y formatos diversos | Números, fechas, texto libre y listas guardadas como texto |
| Veracidad | Calidad y fiabilidad | El 97,2 % sin salario anual, habilidades repetidas, sesgos |
| Valor | Utilidad de lo que se extrae | ¿Qué habilidades conviene aprender? |

Las tres primeras V vienen de Laney (2001). Las 5 V son una convención didáctica, no un estándar.

## 2. Ciclo de vida de los datos

Generación → ingesta → almacenamiento → procesamiento → análisis → visualización y comunicación → archivo o borrado.

| Fase | Qué puede hacer la IA | Riesgo |
|---|---|---|
| Ingesta | Escribir scripts de descarga y conversión | Rutas o formatos supuestos sin comprobar |
| Almacenamiento | Proponer formato (Parquet) y esquema | Tipos mal inferidos |
| Procesamiento | Generar SQL o código | Lógica incorrecta o que no escala |
| Análisis | Interpretar resultados | Inventar o sobreinterpretar |
| Comunicación | Redactar informes | Cifras que no se pueden rastrear |

## 3. Escalado y procesamiento distribuido

- **Vertical:** más RAM y CPU en una máquina. Tiene techo y el coste crece rápido.
- **Horizontal:** repartir el trabajo entre varias máquinas.
- **MapReduce** (Dean y Ghemawat, 2004): *map* procesa cada trozo por separado; *reduce* combina los resultados parciales. **Hadoop** lo implementa con **HDFS**, que reparte y replica los bloques entre máquinas y guarda en disco los resultados intermedios.
- **Spark:** el mismo reparto, pero con los datos intermedios en memoria. Suele ser mucho más rápido en cálculos que repiten pasos.
- **Motores locales como DuckDB:** procesan por columnas y por bloques usando todos los núcleos. Un portátil analiza hoy datos que hace una década pedían un clúster.
- **El límite:** lo que cabe en el disco de una máquina, y la red cuando los datos están lejos. Con Amazon Reviews 2023 (571 millones de reseñas), contar 25,6 millones de reseñas por red tarda 9 s porque solo lee metadatos, pero agruparlas no termina en 8 minutos porque hay que descargar la columna.
- **Batch y streaming:** procesar por lotes (lo que hacemos en la demo) o de forma continua conforme llegan los datos (Kafka, Flink).

**Medido con `measure_memory.py`** (mediana del salario por puesto sobre 785.741 filas):

| Método | Memoria pico | Tiempo |
|---|---|---|
| pandas, CSV completo en memoria | 751 MB | 2,5 s |
| pandas, Parquet leyendo solo 2 columnas | 157 MB | 1,5 s |
| DuckDB sobre el CSV | 183 MB | 0,8 s |
| DuckDB sobre el Parquet | 44 MB | 0,3 s |

Una sola ejecución en un portátil Windows con 16 GB de RAM. En tu equipo variarán: puedes medirlos con `uv run scripts/measure_memory.py`.

**Regla práctica:** no cargues todo en memoria. Pide al motor que agregue y trae solo el resultado.

## 4. Almacenamiento: formatos y arquitecturas

- **Por filas** (CSV, bases de datos transaccionales): bueno para leer o escribir un registro completo.
- **Por columnas** (Parquet): bueno para analítica. Solo se lee lo necesario, y los valores de una misma columna se parecen entre sí, así que comprimen mejor.
- Parquet conserva los tipos (el CSV solo es texto) y guarda estadísticas por bloque que permiten saltarse datos, e incluso contar filas sin leerlas.
- **En la demo:** 231 MB de CSV pasan a 39 MB de Parquet, unas 6 veces menos.
- **Data warehouse:** datos limpios y estructurados para consultas de negocio. **Data lake:** datos en bruto de cualquier tipo, baratos de guardar. **Lakehouse:** ficheros abiertos como Parquet en un lago, con las garantías de un warehouse.

## 5. Estructurados, semiestructurados y no estructurados

- **Estructurados:** tablas con un esquema fijo.
- **Semiestructurados:** JSON, XML o listas dentro de un campo, como `job_skills`.
- **No estructurados:** texto libre, imágenes, audio, vídeo. Son la mayoría de los datos que se generan.
- La IA ayuda a darles estructura: clasificar, extraer entidades, resumir. Pero **cada valor que produce es una predicción con error**. Con `classify_text.py`, el modelo de Hugging Face acierta la estrella exacta de una reseña el 46 % de las veces y se queda a una estrella o menos el 90 %, sobre 200 reseñas en español.
- **Hugging Face** es una plataforma abierta para publicar y compartir datasets y modelos de aprendizaje automático. DuckDB lee sus datasets directamente: `hf://datasets/usuario/nombre/fichero.parquet`.

## 6. Calidad de datos: las reglas que importan

- Un NULL no es un cero: di cuántos hay y cómo los has tratado.
- Contar entidades (ofertas) no es contar menciones (habilidades).
- Una cifra sin su n no es una cifra.
- Con valores extremos, mediana mejor que media: el salario medio es 123.286 dólares y el mediano 115.000.
- Un subconjunto con valor (las ofertas con salario) puede no representar al total.
- Reproducibilidad: la misma consulta con los mismos datos da el mismo resultado. Se comprueba con la huella del CSV de resultados.

## 7. Niveles para guiar a la IA

| Nivel | Qué es | Resuelve | Límite |
|---|---|---|---|
| Prompt | Instrucción puntual | Pedir algo concreto | Se pierde y hay que repetirlo |
| CLAUDE.md | Instrucciones permanentes del proyecto | Reglas que se cargan siempre | Es contexto: no se hace cumplir; debe ser corto |
| Skills | Carpetas de conocimiento bajo demanda | Saber específico sin llenar el contexto | La IA decide cuándo usarlas, por su descripción |
| MCP | Conexión a datos y herramientas externas | Acceso directo y límites técnicos (solo lectura) | Seguridad: lo externo puede traer instrucciones maliciosas |
