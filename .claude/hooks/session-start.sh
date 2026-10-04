#!/bin/bash
# Hook SessionStart: instala dependencias para poder correr pruebas y linters
# en sesiones remotas (Claude Code en la nube). Idempotente y no interactivo.
set -euo pipefail

# Solo en entornos remotos (cloud); en local no hace nada.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# Instalación editable con dependencias de desarrollo (pytest, ruff, mypy).
# Se usa `pip install` (no un lockfile) para aprovechar el caché del contenedor.
python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore -e ".[dev]"
