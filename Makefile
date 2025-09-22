PY=python
.PHONY: build render-start install collectstatic migrate clean

install:
	uv pip install --system -r requirements.txt

migrate:
	$(PY) manage.py migrate --noinput

collectstatic:
	$(PY) manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	./.venv/bin/python -m pip show django || true
	./.venv/bin/python manage.py migrate --noinput && \
	./.venv/bin/gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)

clean:
	rm -rf .venv

test:
	pytest

start:
	$(PY) manage.py runserver 0.0.0.0:8000
