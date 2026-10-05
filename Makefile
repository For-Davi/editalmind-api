.DEFAULT_GOAL := help
.PHONY: help install run lint format test-unit test-integration test verify

help: ## List available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-17s %s\n", $$1, $$2}'

install: ## Install dependencies and git hooks
	uv sync
	uv run pre-commit install

run: ## Start the API with auto-reload on http://localhost:8000
	uv run uvicorn editalmind.main:create_app --factory --reload --port 8000

lint: ## Check lint, formatting and types
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src tests

format: ## Fix lint issues and format the code
	uv run ruff check --fix .
	uv run ruff format .

test-unit: ## Run unit tests
	uv run pytest tests/unit

test-integration: ## Run integration tests
	uv run pytest tests/integration

test: ## Run every test with coverage
	uv run pytest --cov --cov-report=term-missing --cov-report=xml

verify: lint test ## Run the same steps as the CI pipeline, including the image build
	docker build -t editalmind-api:verify .
