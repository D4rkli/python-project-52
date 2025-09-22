#!/usr/bin/env bash
set -euxo pipefail

python -V
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

