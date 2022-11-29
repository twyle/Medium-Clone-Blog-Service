update:
	@pip install --upgrade pip

install:
	@pip install -r requirements.txt

install-dev:
	@pip install -r requirements-dev.txt

run:
	@gunicorn -b 0.0.0.0:5000 manage:app

test:
	@docker-compose -f tests/database/docker-compose.yml down -v
	@docker-compose -f tests/database/docker-compose.yml up --build -d
	@python -m pytest

pre-commit:
	@pre-commit install

initial-tag:
	@git tag -a -m "Initial tag." v0.0.1

init-cz:
	@cz init

bump-tag:
	@cz bump --check-consistency --changelog

start-db-containers:
	@sudo docker-compose -f database/docker-compose.yml up --build -d

stop-db-containers:
	@sudo docker-compose -f sdatabase/docker-compose.yml down -v

create-db:
	@python manage.py create_db

seed-db:
	@python manage.py seed_db

test-local:
	@curl localhost

build:
	@docker build -f Dockerfile.dev -t blog-service:latest .

tag:
	@docker tag blog-service:latest lyleokoth/blog-service:latest

push:
	@docker login
	@docker push lyleokoth/blog-service:latest

run-dev:
	@docker run -p5000:5000 --env-file=./.env blog-service:latest

stop-dev:
	@docker-compose -f docker-compose-dev.yml down

coverage:
	@coverage run -m pytest
	@coverage report -m

lint:
	@isort .
	@black .
	@flake8
	@pylint --rcfile=.pylintrc ./api

#pattern: (build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)(\(\S+\))?!?:(\s.*)
