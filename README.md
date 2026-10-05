# Business Operations Platform

A production-style REST API for managing business operations (employees), built with FastAPI, PostgreSQL, and Docker. Includes JWT authentication, a service-layer architecture, automated tests, and structured logging.

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **Alembic** — database migrations
- **JWT (python-jose) + Passlib/bcrypt** — authentication and password hashing
- **Docker & Docker Compose** — containerized app + database
- **Pytest** — automated testing

## Architecture

Routes (`main.py`) → Services (`services/`) → Data access (`crud.py`) → Database

- **Routes** handle HTTP concerns only (request/response shape, status codes)
- **Services** contain business logic and error handling
- **CRUD layer** is pure database access, no HTTP awareness

## Features

- Full CRUD REST API for Employees
- JWT-based authentication (register, login, protected routes)
- Alembic-managed database migrations
- Structured logging for key business events
- Environment-based configuration (local vs. Docker)
- 13 automated tests covering CRUD, auth, and authorization

## Running Locally (without Docker)

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
### edit .env with your local database credentials

docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload

API available at `http://127.0.0.1:8000`, interactive docs at `http://127.0.0.1:8000/docs`.

## Running with Docker (full stack)

cp .env.example .env
### edit .env with your own values (see note below)

docker compose up --build -d
docker compose exec app alembic upgrade head

API available at `http://localhost:8000`.

**Note:** `.env`'s `DATABASE_URL` should use `localhost` for local runs. Docker Compose builds its own internal `DATABASE_URL` (using the `db` service name) from the `POSTGRES_*` variables — this is intentional, since `db` only resolves inside the Docker network.

## Running Tests

docker compose up -d db
pytest -v

## API Overview

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| POST | `/register` | No | Create a new user account |
| POST | `/login` | No | Log in, returns JWT access token |
| GET | `/employees/` | No | List employees |
| GET | `/employees/{id}` | No | Get one employee |
| POST | `/employees/` | Yes | Create an employee |
| PATCH | `/employees/{id}` | Yes | Update an employee |
| DELETE | `/employees/{id}` | Yes | Delete an employee |

Protected routes require an `Authorization: Bearer <token>` header, obtained from `/login`.

## Project Structure

app/
- main.py — FastAPI routes
- models.py — SQLAlchemy ORM models
- schemas.py — Pydantic request/response schemas
- crud.py — Pure database access
- services/ — Business logic layer
- security.py — Password hashing, JWT handling
- database.py — DB connection/session setup
- logging_config.py — Logging configuration

alembic/ — Database migrations
tests/ — Pytest test suite
