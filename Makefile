#!/usr/bin/make

.PHONY: all

all:
	@docker compose -f compose.dev.yml up --build

down:
	@docker compose -f compose.dev.yml down