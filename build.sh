#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"
source "$HOME/.local/bin/env"

uv venv .venv
source .venv/bin/activate

uv pip install .

python manage.py collectstatic --noinput
python manage.py migrate

