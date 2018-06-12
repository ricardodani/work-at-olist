build:
	@docker-compose build

_db:
	@docker-compose up -d db

migrate: _db
	@docker-compose run web python manage.py migrate

static: _db
	@docker-compose run web python manage.py collectstatic --noinput

superuser: _db
	@docker-compose run web python manage.py createsuperuser

run: build migrate static
	@docker-compose up

run-dev: _db
	@docker-compose run --service-ports -e DEBUG=1 web python manage.py runserver 0:8000

test:
	@docker-compose run web python manage.py test

shell: _db
	@docker-compose run web python manage.py shell

docs:
	@docker-compose run web sphinx-build -b html docs/source docs/build
