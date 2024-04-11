#!/usr/bin/make

DEV=docker compose -f compose.dev.yml
PROD=docker compose -f compose.dev.yml -f compose.prod.yml

.PHONY: all dev prod down refresh clean

all: dev

dev:
	@echo "Starting up DEV mode."
	$(DEV) up -d --build

down:
	@echo "Shutting down..."
	$(PROD) down

prod:
	@echo "Starting up PROD services..."
	$(PROD) up -d --build

.PHONY: refresh
refresh:
	$(PROD) down
	$(DEV) up -d --build --remove-orphans

.PHONY: clean
clean:
	@echo "Cleaning up services..."
	$(PROD) down -v
	sudo rm -rf .logs .volumnes