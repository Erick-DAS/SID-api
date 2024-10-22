.PHONY: help
help: # Show help for each of the Makefile recipes.
	@echo
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
	@echo

.PHONY: migrate-generate
migrate-generate: # Generates an alembic migration. Accepts a name also
	@read -p "Digite o nome da nova migration: " migration_name; \
	echo "Criando a migration '$$migration_name'..."; \
	alembic revision --autogenerate -m "$$migration_name"

.PHONY: migrate
migrate: # Execute alembic migrations
	@alembic upgrade head

.PHONY: migrate-undo
migrate-undo: # Undo the last executed alembic migration
	@alembic downgrade -1

.PHONY: run-api
run-api: # Runs the API with FastAPI. Swagger at localhost:8000/docs and documentation at localhost:8000/redoc
	@fastapi run app/main.py

.PHONY: run-db
run-db: # Runs the database with docker-compose
	@docker compose up -d

.PHONY: stop-db
stop-db: # Stops the database container maintaining all the data
	@docker compose stop

.PHONY: destroy-db
destroy-db: # Kills the database container removing all the data
	@docker compose down

.PHONY: install
install: # Installs the dependencies with poetry
	@poetry install --no-root

.PHONY: start-venv
start-venv: # Starts poetry virtual environment. ALWAYS run this before starting to code
	@poetry shell

.PHONY: format
format: # Formats the code with ruff
	@ruff format

.PHONY: lint-check
lint-check: # Checks for lint errors with ruff. Really mediocre linter
	@ruff check

.PHONY: lint
lint: # Fixes some ruff detected lint errors
	@ruff check --fix
