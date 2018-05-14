build:
	@docker-compose build

_db:
	@docker-compose up -d db

migrate: _db
	@docker-compose run web python manage.py migrate

run: build migrate
	@docker-compose up

