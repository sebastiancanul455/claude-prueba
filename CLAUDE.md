# CLAUDE.md

Guía para Claude Code en este repositorio. Responde al usuario en **español**.

## Contexto del proyecto

Herramientas en Python para física médica y radioterapia, con interés a futuro en
entrenar modelos de IA para uso en la clínica. El usuario es físico médico en un centro
grande de radioterapia.

## Comandos

```bash
pip install -e ".[dev]"   # instalar (en sesiones remotas lo hace el hook de SessionStart)
python -m pytest          # pruebas
python -m ruff check .    # linter
python -m ruff format .   # formato
python -m mypy            # chequeo de tipos (strict, solo src/)
```

> Usar siempre `python -m <herramienta>`. En las sesiones remotas los ejecutables `pytest`,
> `mypy` y `ruff` del PATH son versiones aisladas (uv) que no ven los paquetes instalados
> con pip; invocarlos como módulo usa el mismo Python en el que se instaló el proyecto.

## Estructura

- `src/claude_prueba/` — paquete (layout `src/`).
- `tests/` — pruebas con pytest; un archivo `test_<modulo>.py` por módulo.
- `.claude/hooks/session-start.sh` — instala dependencias en sesiones remotas (cloud).

## Convenciones de código

- Python >= 3.10, con type hints en toda la API pública (mypy `strict`).
- Docstrings y comentarios en español.
- **Unidades explícitas** en nombres y docstrings (`x_mm`, `dosis_gy`, `dta_mm`); nunca unidades implícitas.
- Funciones puras y pequeñas; sin rutas ni constantes de la clínica escritas en el código.
- Todo cambio de lógica lleva su prueba. Para dosimetría, probar casos con respuesta analítica conocida.

## 🔒 Privacidad y datos clínicos (importante)

- **Nunca** subir, pegar, leer ni versionar datos reales de pacientes (DICOM, planes,
  nombres, números de expediente, fechas de nacimiento). Solo datos sintéticos o anonimizados.
- Si aparece un archivo que parezca contener información de pacientes, no lo abras ni lo
  copies; avisa al usuario.
- Los datos sintéticos se generan por código (ver `claude_prueba.dosimetria.perfil_gaussiano`).

## ⚕️ Uso clínico

El código aquí es experimental y **no está validado para uso clínico**. No presentar
resultados como clínicamente válidos. Todo lo destinado a pacientes requiere verificación
y validación formales por el físico médico responsable.

## Git

- Desarrollar en la rama asignada a la sesión; hacer commits claros y push a esa rama.
- No crear Pull Requests salvo que el usuario lo pida explícitamente.
