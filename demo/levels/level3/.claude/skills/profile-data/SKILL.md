---
name: profile-data
description: Perfila un dataset antes de analizarlo (filas, columnas, tipos, % de nulos, duplicados, columnas que parecen listas o JSON). Úsala siempre que se vaya a analizar una tabla nueva o el usuario pida perfilar, explorar o conocer los datos.
---

# Perfilar los datos antes de analizar

Haz esto ANTES de cualquier cálculo y responde con una ficha corta.

1. **Tamaño:** número de filas y columnas (`SELECT count(*)`, `DESCRIBE jobs`).
2. **Nulos:** % de NULL por columna. Marca las que superen el 30 %.
3. **Tipos sospechosos:** columnas de texto que parecen listas, JSON o fechas. Enseña 3 valores reales con `LIMIT 3`.
4. **Identificador:** comprueba si hay una clave única (`count(*) = count(DISTINCT col)`). Si no la hay, avisa.
5. **Duplicados:** cuántas filas se repiten.
6. **Rangos:** mínimo, máximo y mediana de las columnas numéricas. Señala valores imposibles (negativos, ceros, extremos).

Salida: una tabla `columna | tipo | % nulos | observación` y una lista de «riesgos para el análisis».
Atajo para los puntos 1 y 2: `uv run ../../scripts/demo/profile_dataset.py`.

En esta fase no saques conclusiones sobre el tema: solo describe los datos.
