#!/usr/bin/env bash
set -euo pipefail

# 1) ставим uv на билд-окружение
curl -LsSf https://astral.sh/uv/install.sh | sh
# подключаем env, чтобы появились uv/uvx в PATH
# shellcheck disable=SC1090
source "$HOME/.local/bin/env"

# 2) установка зависимостей и прогон подготовительных команд
make install
make collectstatic
make migrate
