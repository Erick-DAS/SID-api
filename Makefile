migrate-generate:
	alembic revision --autogenerate -m "migration message"

migrate:
	alembic upgrade head

migrate-undo:
	alembic downgrade -1

run-api:
	fastapi run app/main.py

run-db:
	docker compose up -d

stop-db: 
	docker compose stop

destroy-db:
	docker compose down

install:
	poetry install --no-root

start-venv:
	poetry shell

