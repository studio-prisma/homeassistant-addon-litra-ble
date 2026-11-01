#!/usr/bin/env bash
# Runs every local check CI runs. Needs Python 3.9+ and PyYAML.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m compileall -q litra_ble_bridge/litra_ble litra.py tests
python3 - <<'PY'
import yaml
for path in ("litra_ble_bridge/config.yaml", "litra_ble_bridge/build.yaml", "repository.yaml"):
    with open(path, encoding="utf-8") as f:
        yaml.safe_load(f)
print("yaml ok")
PY
python3 -m unittest discover -s tests -v
