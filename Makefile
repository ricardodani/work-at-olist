build:
	@docker-compose build

_db:
	@docker-compose up -d db

migrate: _db
	@docker-compose run web python manage.py migrate

superuser: _db
	@docker-compose run web python manage.py createsuperuser

run: migrate
	@docker-compose up

run-dev: _db
	@docker-compose run --service-ports web python manage.py runserver 0:8000

test:
	@docker-compose run web python manage.py test

shell: _db
	@docker-compose run web python manage.py shell

_docs:
	@docker-compose run web sphinx-build -b html docs/source docs/build

docs: _docs
	@open phonebillapi/docs/build/index.html
