# editalmind-api

[![ci](https://github.com/For-Davi/editalmind-api/actions/workflows/ci.yml/badge.svg)](https://github.com/For-Davi/editalmind-api/actions/workflows/ci.yml)

Core API of [EditalMind](https://github.com/For-Davi/editalmind): authentication, exam notices, study plans, subscriptions and performance tracking.

**Stack:** Python 3.12, FastAPI, Pydantic v2, pydantic-settings, uv, Ruff, mypy (strict), pytest.

## Architecture

The code follows Clean Architecture ([ADR-003](https://github.com/For-Davi/editalmind/blob/main/docs/adr/003-clean-architecture.md)); the dependency rule is enforced by `tests/unit/test_architecture.py`.

```text
src/editalmind/
├── domain/           # entities, value objects, events, ports (no framework imports)
├── application/      # use cases
├── infrastructure/   # adapters: databases, queues, storage, settings
├── presentation/     # FastAPI routers and HTTP schemas
└── main.py           # composition root (create_app)
tests/
├── unit/             # no database, network or LLM
└── integration/      # the app over HTTP; real databases via Testcontainers
```

## Running

```bash
make install   # uv sync + pre-commit hooks
make run       # http://localhost:8000/health and http://localhost:8000/docs
```

Configuration comes from environment variables prefixed with `API_` (see `.env.example`). The databases are provided by [editalmind-infra](https://github.com/For-Davi/editalmind-infra).

## Quality

```bash
make lint               # ruff check + ruff format --check + mypy strict
make test-unit
make test-integration
make test               # both, with coverage (fails under 80%)
```

The CI pipeline runs lint, tests and the Docker build on every pull request, and publishes the image to `ghcr.io` on every push to `main`.

## Docker

```bash
docker build -t editalmind-api .
docker run --rm -p 8000:8000 editalmind-api
```

Multi-stage build with uv, non-root user and a `HEALTHCHECK` on `/health`.
