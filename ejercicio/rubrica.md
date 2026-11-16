# Rúbrica (10 puntos)

| Criterio | Peso | 0 | La mitad | Completo |
|---|---|---|---|---|
| **Pregunta y datos:** pregunta concreta, dataset de al menos 100.000 filas, origen y licencia indicados | 0,5 | Pregunta vaga o dataset pequeño | Falta origen o licencia, o la pregunta es amplia | Clara, respondible y bien documentada |
| **CLAUDE.md:** reglas que resuelven fallos reales y observados | 1,5 | Genérico o copiado | Algunas reglas útiles, otras de relleno | Al menos 6 reglas, cada una ligada a un fallo del informe |
| **Skills:** conocimiento específico del dataset y del método, con una descripción que se activa bien | 2,0 | Sin Skills o son la plantilla | Correctas pero genéricas | Propias, útiles y con las trampas reales del dataset |
| **MCP:** conexión a los datos en solo lectura | 0,5 | Sin MCP | Configurado pero sin probar | Configurado, probado y con el límite de solo lectura explicado |
| **Datos no estructurados:** columna creada con un modelo de Hugging Face | 1,0 | No hay | Hecha sin medir el error | Muestra justificada y error medido frente a etiquetas reales |
| **Análisis y reproducibilidad:** SQL en `queries/`, `reproduce.py --check` correcto, sin rutas absolutas | 1,5 | No se reproduce | Se reproduce con ajustes manuales | Se reproduce a la primera en otro equipo |
| **Informe y verificación crítica:** n en cada cifra, limitaciones honestas, al menos 3 errores de la IA | 2,0 | Solo celebra resultados | Errores listados sin explicar cómo se detectaron | Errores reales, con la evidencia de la detección y la corrección aplicada |
| **Revisión cruzada:** checklist completada de un compañero y correcciones aplicadas | 1,0 | No hecha | Hecha sin hallazgos útiles | Hallazgos concretos y resueltos |

## Penalizaciones

- Datos, claves o rutas personales subidos al repositorio: -1.
- Cifras del informe que no salen de `results/`: -1 por cada cifra inventada o no verificable.
- `validate_submission.py` con errores: la entrega no se considera completa.

## Sobre el validador

`validate_submission.py` comprueba la estructura, no la calidad. La calidad se evalúa con esta rúbrica y con la reproducción por un compañero.
