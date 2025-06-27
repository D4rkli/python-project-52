install:
	uv pip install -r pyproject.toml

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi


