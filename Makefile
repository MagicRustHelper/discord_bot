dev:
	docker compose -f "docker-compose.dev.yml" -p "discord-dev" up --build -d

build:
	docker compose -f "docker-compose.prod.yml" -p "discord" up --build -d

run-prod:
	alembic upgrade head
	python3 -m app