install:
	uv pip install .

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	.venv/bin/gunicorn task_manager.wsgi
