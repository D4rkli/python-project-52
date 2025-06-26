#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

$HOME/.local/bin/uv venv .venv

source .venv/bin/activate

$HOME/.local/bin/uv pip install --python .venv/bin/python .

python manage.py collectstatic --noinput
python manage.py migrate


