PY=python

install:
	uv pip install --system -r requirements.txt

migrate:
	$(PY) manage.py migrate --noinput

collectstatic:
	$(PY) manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	python manage.py migrate --noinput && gunicorn task_manager.wsgi:application --bind 0.0.0.0:$(PORT)

test:
	pytest

start:
	$(PY) manage.py runserver 0.0.0.0:8000
