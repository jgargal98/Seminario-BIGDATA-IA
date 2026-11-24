# Seminario: Big Data con IA

Cómo guiar a un asistente de IA (Claude Code) para analizar grandes volúmenes de datos de forma fiable: sin inventar resultados, respetando los límites de los datos y de forma que otra persona pueda repetirlo.

## Preparación

Hazlo **antes del día del seminario**. Desde la carpeta del repositorio:

```bash
uv run scripts/install/check_setup.py
```

Este comando instala Python y las librerías del proyecto, descarga los datos de la demo y el modelo de IA (alrededor de 1,5 GB la primera vez), prepara el servidor MCP y comprueba que todo funciona. Puede tardar varios minutos. Al final tiene que decir **«Todo listo para el seminario»**.

- Si se interrumpe, vuelve a ejecutarlo: sigue por donde lo dejó.
- Los avisos no impiden seguir; los fallos sí, y cada uno dice cómo arreglarlo.

**Opcional:** inicia sesión en Hugging Face para tener límites de descarga más altos. Ejecuta este comando y sigue los pasos en el navegador:

```bash
uv run hf auth login
```

### Si aún no tienes los programas

Necesitas un portátil con Windows, Mac o Linux, 8 GB de RAM y 5 GB libres; un plan Pro de Claude; y una cuenta de GitHub. Instala:

- **Git:** <https://git-scm.com/downloads>
- **Claude Code:** <https://code.claude.com/docs/en/setup>
- **uv:** <https://docs.astral.sh/uv/getting-started/installation/>

El chat normal de Claude no sirve: hace falta Claude Code, que trabaja sobre las carpetas de tu ordenador.

Después, cierra la terminal y abre una nueva, clona el repositorio y entra en él:

```bash
git clone https://github.com/jgargal98/Seminario-BIGDATA-IA.git
```

```bash
cd Seminario-BIGDATA-IA
```

## Demo

La demo tiene 4 niveles acumulativos: 1 solo prompt, 2 CLAUDE.md, 3 Skills, 4 MCP. Se hace en una carpeta aparte, `seminario-demo`, que se crea al lado del repositorio: así, en cada nivel Claude solo tiene lo que ese nivel le da.

Hacen falta dos terminales. En la primera, desde la raíz del repositorio, prepara un nivel:

```bash
uv run scripts/demo/prepare_demo.py --level 2
```

En la segunda, abre Claude Code en la carpeta de la demo:

```bash
cd ../seminario-demo
```

```bash
claude
```

Cada vez que preparas un nivel, `seminario-demo` se vacía: lo que hayas hecho en el nivel anterior se pierde. Sal de Claude (`/exit`) antes de preparar otro nivel y vuelve a abrirlo después: Claude solo lee el CLAUDE.md, las Skills y el MCP al arrancar.

## Ejercicio

El enunciado de la práctica os lo entregará el profesor en PDF. Los datasets entre los que elegir están en [catalogo_datasets.md](catalogo_datasets.md).

## Estructura

| Ruta | Contenido |
|---|---|
| `pyproject.toml`, `uv.lock` | Librerías del proyecto y sus versiones exactas |
| `scripts/install/` | Preparación del ordenador |
| `scripts/demo/` | Scripts que usa la demo |
| `scripts/common.py` | Ajustes compartidos por los scripts |
| `demo/levels/` | CLAUDE.md del nivel 2 y Skills del nivel 3 |
| `catalogo_datasets.md` | Datasets entre los que elegir para la práctica |

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `uv` o `claude` no se reconocen como comando | Cierra la terminal y abre una nueva. |
| `claude` sigue sin reconocerse en Windows | El instalador no lo añadió al PATH. En PowerShell: `[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:USERPROFILE\.local\bin", "User")` y abre una terminal nueva. |
| PowerShell no permite ejecutar scripts | Sigue las instrucciones para Windows de la [página de instalación de uv](https://docs.astral.sh/uv/getting-started/installation/). |
| La descarga se corta (`Connection reset`, `timeout`) | Vuelve a ejecutar `uv run scripts/install/check_setup.py`. Lo ya descargado no se repite. Si sigue fallando, prueba otra red. |
| No hay espacio en disco | Libera al menos 5 GB y vuelve a ejecutar. |
| El servidor `huggingface` pide autenticación en `/mcp` | Selecciónalo en `/mcp` y sigue los pasos en el navegador. |

Claude no es determinista: lo que haga en cada nivel puede variar entre sesiones.
