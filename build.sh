#!/usr/bin/env bash
set -euxo pipefail

python -m venv .venv
./.venv/bin/python -V
./.venv/bin/python -m pip install --upgrade pip setuptools wheel
./.venv/bin/python -m pip install -r requirements.txt

./.venv/bin/python manage.py collectstatic --noinput

