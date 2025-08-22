# Variables
DOCKER_COMPOSE := docker compose

# Help target (default)
help:
	@echo "Available commands:"
	@echo "  make build       - Build the Docker image"
	@echo "  make shell       - Enter docker web django shell"
	@echo "  make bash       - Enter docker web django bash"
	@echo "  make start       - Start the application stack"
	@echo "  make stop        - Stop the application stack"
	@echo "  make restart     - Restart the application stack"
	@echo "  make migrate     - Run Django migrations"
	@echo "  make makemigrations     - Run Django migrations"
	@echo "  make test        - Run Django tests"
	@echo "  make clean       - Remove containers"

# Build the Docker image
build:
	@$(DOCKER_COMPOSE) build

# Start the application stack
start:
	@$(DOCKER_COMPOSE)  up web

# Bash
bash:
	@$(DOCKER_COMPOSE) exec -it web bash

# Shell
shell:
	@$(DOCKER_COMPOSE) exec -it web bash -c "python manage.py shell"

# Stop the application stack
stop:
	@$(DOCKER_COMPOSE) down

# Restart the application stack
restart: stop start

# Run Django migrations
makemigrations:
	@$(DOCKER_COMPOSE) run --rm web python manage.py makemigrations

migrate:makemigrations
	@$(DOCKER_COMPOSE) run --rm web python manage.py migrate

# Run Django tests
test:
	@$(DOCKER_COMPOSE) run --rm web python manage.py test

# Clean up containers and volumes
clean:
	@$(DOCKER_COMPOSE) down --volumes --remove-orphans

# Tail logs from all services
logs:
	@$(DOCKER_COMPOSE) logs -f

lint-local:
	black --line-length=88 file_summary  tests/ && isort file_summary/ tests/

.PHONY: help build start stop restart migrate test clean logs lint-local makemigrations migrate
