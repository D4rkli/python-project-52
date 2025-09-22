#!/usr/bin/env bash
set -euxo pipefail

curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

uv pip install --system -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

