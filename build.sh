#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv pip install .

python manage.py collectstatic --noinput
python manage.py migrate
