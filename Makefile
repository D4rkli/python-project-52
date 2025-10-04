PY=python
.PHONY: build render-start install collectstatic migrate clean

install:
	uv pip install --system -r requirements.txt

migrate:
	$(PY) manage.py migrate --noinput

collectstatic:
	$(PY) manage.py collectstatic --noinput

build:
	python -m venv .venv
	./.venv/bin/python -m pip install --upgrade pip wheel setuptools
	./.venv/bin/python -m pip install .
	./.venv/bin/python -m pip install "gunicorn>=21,<22"

render-start:
	./.venv/bin/python manage.py migrate --noinput
	./.venv/bin/python manage.py collectstatic --noinput
	PORT=$$PORT ./\.venv/bin/gunicorn task_manager.wsgi:application \
		--bind 0.0.0.0:$$PORT --workers 3 --timeout 60

clean:
	rm -rf .venv .pytest_cache .mypy_cache dist build *.egg-info

test:
	pytest

start:
	$(PY) manage.py runserver 0.0.0.0:8000
