# claude-prueba

Proyecto de pruebas en Python para herramientas de **física médica y radioterapia**.

> ⚠️ **Aviso:** el código de este repositorio es de carácter educativo y experimental.
> **No está validado para uso clínico.** Cualquier herramienta que vaya a usarse con
> pacientes requiere verificación y validación formales por el físico médico responsable.

## 🔒 Privacidad

Este repositorio **no debe contener datos reales de pacientes** (DICOM, planes, nombres,
números de expediente). Usa datos sintéticos o debidamente anonimizados. El `.gitignore`
bloquea por defecto los archivos `*.dcm`.

## 🚀 Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 🧪 Desarrollo

```bash
python -m pytest            # pruebas
python -m ruff check .      # linter
python -m ruff format .     # formato
python -m mypy              # tipos
```

## 📁 Estructura

```
src/claude_prueba/     código del paquete
tests/                 pruebas (pytest)
.claude/               configuración de Claude Code (hook de inicio de sesión)
.github/workflows/     integración continua
```

## 📌 Contenido actual

- `claude_prueba.dosimetria`: perfil gaussiano sintético e índice gamma 1D (ejemplo).

## 🗺️ Próximos pasos sugeridos

- Lectura de archivos DICOM-RT con `pydicom` (usando solo datos sintéticos/anonimizados).
- Análisis gamma 2D/3D con interpolación.
- Pipelines de entrenamiento de modelos de IA con evaluación reproducible.
