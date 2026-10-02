#!/usr/bin/env bash
# Regenera configs/, docs/cambios/, docs/03, docs/04 y el informe de validación a partir de originales/.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf configs docs/cambios
python3 tools/generar_cfx.py
python3 tools/validar_cfx.py
python3 tools/generar_fichas.py
python3 tools/generar_guia.py
