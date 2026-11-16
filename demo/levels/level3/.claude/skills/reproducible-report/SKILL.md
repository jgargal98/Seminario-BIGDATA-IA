---
name: reproducible-report
description: Genera el informe final de un análisis con resultados, limitaciones y huellas para que otra persona pueda repetirlo. Úsala cuando el usuario pida un informe, un resumen final, la entrega o dejar el análisis reproducible.
---

# Informe reproducible

Crea `report.md` con estas secciones y en este orden:

1. **Pregunta:** una frase.
2. **Datos:** origen, licencia, número de filas usadas (n) y filtros aplicados.
3. **Método:** qué consultas (`queries/NN_*.sql`) y en qué orden.
4. **Resultados:** tablas con n en cada cifra.
5. **Limitaciones:** nulos descartados, sesgos de la muestra y qué NO se puede concluir.
6. **Errores de la IA detectados y corregidos:** qué propuso mal, cómo se detectó y qué cambio lo evita.
7. **Cómo reproducirlo:** los comandos exactos.

## Antes de terminar
- Ejecuta `uv run ../../scripts/demo/reproduce.py` (genera `results/*.csv` y `results/fingerprints.json`).
- Ejecútalo otra vez con `--check`: tiene que terminar en REPRODUCIBLE.
- No pongas en el informe ninguna cifra que no salga de `results/`.
- Si algo no se pudo verificar, escríbelo en Limitaciones en vez de omitirlo.
