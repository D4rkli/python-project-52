#!/usr/bin/env bash
set -euxo pipefail

python -V

python -m venv .venv
. .venv/bin/activate

pip install -U pip setuptools wheel
pip install -r requirements.txt

python manage.py collectstatic --noinput


