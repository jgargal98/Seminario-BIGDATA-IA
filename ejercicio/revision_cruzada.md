# Checklist de revisión cruzada

Revisor/a: ____________  Autor/a revisado/a: ____________  Fecha: ________

## A. Reproducir (en TU ordenador, sin ayuda del autor)

- [ ] Clono el repositorio y sigo SOLO su README. Pasos donde me atasco: ______________________
- [ ] `uv sync` funciona.
- [ ] El script de descarga y preparación de datos funciona.
- [ ] `uv run scripts/reproduce.py --check` termina en REPRODUCIBLE.
- [ ] `uv run scripts/validate_submission.py .` no da errores.
- [ ] Con mi propio Claude y su CLAUDE.md y Skills, una de sus subpreguntas da el mismo resultado.

Tiempo que he necesitado: ____ min

## B. Contenido

- [ ] Cada cifra del informe aparece en `results/*.csv` y lleva su n.
- [ ] Cada regla de CLAUDE.md tiene sentido para ESTE dataset (¿hay alguna de relleno?).
- [ ] Las Skills describen cuándo usarlas y contienen conocimiento real del dataset.
- [ ] La columna creada con el modelo de Hugging Face tiene su error medido.
- [ ] El informe lista errores concretos de la IA: qué, cómo se detectó y cómo se corrigió.
- [ ] Hay alguna trampa del dataset que el autor no ha detectado: ______________________

## C. Resultado

Hallazgos que el autor debe corregir, por orden de importancia:

1.
2.
3.

Valoración global: [ ] se reproduce tal cual  [ ] con ajustes menores  [ ] no se reproduce
