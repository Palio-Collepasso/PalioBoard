SHELL := /bin/sh

API_DIR := apps/api
WEB_DIR := apps/web
COMPOSE_FILE := infra/compose/docker-compose.yml

.DEFAULT_GOAL := help

.PHONY: help up down backend-dev web-dev openapi-export openapi-types test test-backend test-web test-e2e

define require_file
	@if [ ! -f "$(1)" ]; then \
		printf '%s\n' "Missing $(1). This top-level target is reserved for $(2) and will become runnable when $(3) lands."; \
		exit 1; \
	fi
endef

help: ## Show the stable top-level command surface
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_-]+:.*## / {printf "%-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

up: ## Start local infrastructure through Docker Compose
	$(call require_file,$(COMPOSE_FILE),the local stack,TASK-6)
	docker compose -f $(COMPOSE_FILE) up -d

down: ## Stop local infrastructure
	$(call require_file,$(COMPOSE_FILE),the local stack,TASK-6)
	docker compose -f $(COMPOSE_FILE) down

backend-dev: ## Run the backend locally with uv
	$(call require_file,$(API_DIR)/pyproject.toml,the backend app,TASK-2)
	cd $(API_DIR) && uv run fastapi dev src/palio/app/main.py

web-dev: ## Run the Angular app locally with npm
	$(call require_file,$(WEB_DIR)/package.json,the frontend app,TASK-3)
	cd $(WEB_DIR) && npm run start

openapi-export: ## Export the committed OpenAPI spec from the backend app
	$(call require_file,$(API_DIR)/pyproject.toml,the backend app,TASK-2)
	mkdir -p docs/api
	cd $(API_DIR) && uv run python -m palio.app.export_openapi ../../docs/api/openapi.yaml

openapi-types: ## Generate frontend TS types from the committed OpenAPI spec
	$(call require_file,$(WEB_DIR)/package.json,the frontend app,TASK-3)
	$(call require_file,docs/api/openapi.yaml,the committed OpenAPI spec,TASK-7)
	cd $(WEB_DIR) && npm run generate:api-types

test: test-backend test-web test-e2e ## Run all repository test suites

test-backend: ## Run backend tests
	$(call require_file,$(API_DIR)/pyproject.toml,the backend test harness,TASK-8)
	cd $(API_DIR) && uv run pytest tests/unit
	cd $(API_DIR) && uv run pytest tests/integration

test-web: ## Run frontend tests
	$(call require_file,$(WEB_DIR)/package.json,the frontend test harness,TASK-9)
	cd $(WEB_DIR) && npm test -- --watch=false

test-e2e: ## Run Playwright end-to-end tests
	$(call require_file,$(WEB_DIR)/package.json,the end-to-end test harness,TASK-9)
	cd $(WEB_DIR) && npm run e2e
