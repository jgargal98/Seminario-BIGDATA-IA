# Seminario: Big Data con IA

Cómo guiar a un asistente de IA (Claude Code) para analizar grandes volúmenes de datos de forma fiable: sin inventar resultados, respetando los límites de los datos y de forma que otra persona pueda repetirlo.

Haz la instalación **antes del día del seminario**: la primera vez descarga alrededor de 1,5 GB.

Hay una versión paso a paso para los alumnos en [docs/requisitos_alumnos.md](docs/requisitos_alumnos.md).

## Qué necesitas

Portátil con Windows, Mac o Linux, 8 GB de RAM y al menos 5 GB libres en disco. No hace falta instalar Python, Docker ni ninguna base de datos.

### 0. Cuentas (antes de instalar nada)

- **Plan Pro de Claude** (obligatoria): incluye Claude Code; el uso se comparte con el chat.
- **GitHub** (obligatoria, gratis): <https://github.com/signup>
- **Hugging Face** (recomendable, gratis): <https://huggingface.co/join>

## Instalación

Abre una terminal: **PowerShell** en Windows, **Terminal** en Mac o Linux.

### 1. Git

Comprueba si ya lo tienes con `git --version`. Si no:

- **Windows:** `winget install --id Git.Git -e`
- **Mac:** `xcode-select --install`
- **Linux:** con el gestor de paquetes de tu distribución, por ejemplo `sudo apt install git`.

### 2. Claude Code

Claude Code se puede usar de dos formas. Las dos leen el CLAUDE.md, las Skills y el MCP del proyecto. El chat normal de Claude **no** sirve, porque no trabaja sobre las carpetas de tu ordenador.

- **App de escritorio de Claude, pestaña Code:** si ya la tienes, no instales nada más. Descárgala de <https://claude.ai/download> si no la tienes.
- **Terminal (comando `claude`):** es lo que usan los presentadores, porque algunos comandos de la demo (`/mcp`, `/memory`) funcionan mejor ahí.
  - **Windows:** `irm https://claude.ai/install.ps1 | iex`
  - **Mac y Linux:** `curl -fsSL https://claude.ai/install.sh | bash`

### 3. uv

uv instala Python y todas las librerías del proyecto con las mismas versiones para todos.

- **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Mac y Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Cierra la terminal y abre una nueva** para que reconozca los programas que acabas de instalar.

### 4. Descargar el repositorio

```bash
git clone https://github.com/jgargal98/Seminario-BIGDATA-IA.git
```

```bash
cd Seminario-BIGDATA-IA
```

### 5. Instalar y comprobar todo

```bash
uv run scripts/check_setup.py
```

Este comando instala Python y las librerías, descarga los datos de la demo y el modelo de IA, prepara el servidor MCP y comprueba que todo funciona. Puede tardar varios minutos. Al final debe decir **«Todo listo para el seminario»**. Si se interrumpe, vuelve a ejecutarlo: sigue por donde lo dejó.

### 6. Iniciar sesión en Hugging Face (opcional)

Reduce los límites de descarga. Ejecuta este comando y sigue los pasos en el navegador:

```bash
uv run hf auth login
```

### 7. Abrir Claude Code

- **Con la terminal:** escribe `claude` dentro de la carpeta en la que vayas a trabajar.
- **Con la app de escritorio:** abre la pestaña **Code** y elige esa carpeta.

La primera vez te pedirá iniciar sesión con tu cuenta de Claude. En la demo, la carpeta es siempre `demo/session`; en el ejercicio, la raíz de tu repositorio.

## Estructura

| Carpeta | Contenido |
|---|---|
| `scripts/` | Instalación, descarga de datos, perfilado, medición de memoria, clasificación de texto, reproducibilidad y MCP |
| `demo/` | Demo en 4 niveles: `prompts/`, `levels/` (CLAUDE.md y Skills) y `queries/` (consultas de referencia y trampas) |
| `ejercicio/` | Enunciado, rúbrica, revisión cruzada, catálogo de datasets y plantilla para empezar |
| `docs/` | Requisitos, apuntes de teoría y referencias |

## Demo

```bash
uv run scripts/prepare_demo.py --level 2
```

```bash
cd demo/session
```

```bash
claude
```

Con la app de escritorio, en lugar de los dos últimos comandos abre la pestaña **Code** y elige la carpeta `demo/session`.

Los niveles van del 1 al 4 y son acumulativos: 1 solo prompt, 2 CLAUDE.md, 3 Skills, 4 MCP.

## Ejercicio

Lee [ejercicio/enunciado.md](ejercicio/enunciado.md). Antes de entregar:

```bash
uv run scripts/validate_submission.py ruta/a/tu/repositorio
```

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `uv` o `claude` no se reconocen como comando | Cierra la terminal y abre una nueva. |
| `claude` sigue sin reconocerse en Windows | El instalador no lo añadió al PATH. En PowerShell: `[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.local\bin", "User")` y abre una terminal nueva. |
| PowerShell no permite ejecutar scripts | Usa exactamente el comando del paso 3, que ya incluye el permiso necesario. |
| La descarga se corta (`Connection reset`, `timeout`) | Vuelve a ejecutar `uv run scripts/check_setup.py`. Lo ya descargado no se repite. Si sigue fallando, prueba otra red. |
| No hay espacio en disco | Libera al menos 5 GB y vuelve a ejecutar. |
| Sin conexión el día del seminario | Plan B con datos inventados: `uv run scripts/make_synthetic.py` y después `uv run scripts/download_data.py --synthetic`. |
| El servidor MCP de DuckDB no conecta | `uv run scripts/test_mcp.py --config demo/session/.mcp.json` dice qué falla. |
| El servidor `huggingface` pide autenticación en `/mcp` | Selecciónalo en `/mcp` y sigue los pasos en el navegador. |

## Notas

- Claude no es determinista: lo que haga en cada nivel puede variar entre sesiones.
- Las cifras de las Skills y de los apuntes se han comprobado sobre los datos reales. Si algo no te cuadra, compruébalo: es parte del ejercicio.
