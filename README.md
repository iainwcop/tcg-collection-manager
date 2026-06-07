# TCG Collection Manager

A full-stack web application for managing trading card collections — organization, scanning, and live market pricing — built for any collector. Phase 1 focuses on core collection management (binders, boxes, search, and filter).

## Stack

- **Backend:** Django 5 + Django REST Framework
- **Frontend:** React 18 + TypeScript + Vite
- **Database:** PostgreSQL 16
- **Local dev:** Docker Compose

## Quick start

Prerequisites: [Docker](https://docs.docker.com/get-docker/) with Compose.

```bash
# Copy environment defaults (optional — compose has built-in dev defaults)
cp .env.example .env

# Build and start the full stack
docker compose up --build
```

| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/ |
| Health check | http://localhost:8000/api/health/ |
| Django admin | http://localhost:8000/admin/ |

The frontend home page calls the health endpoint to confirm the API is reachable.

### Create a superuser (optional)

```bash
docker compose exec backend python manage.py createsuperuser
```

## Project layout

```
backend/          Django project (apps: users, catalog, collections)
frontend/         React + Vite SPA
docs/             Design documents
docker-compose.yml
```

## API endpoints (boilerplate)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/health/` | No | Health check |
| POST | `/api/auth/register/` | No | Create account |
| POST | `/api/auth/login/` | No | JWT login |
| POST | `/api/auth/refresh/` | No | Refresh JWT |
| GET | `/api/auth/me/` | Yes | Current user |
| CRUD | `/api/collections/` | Yes | User collections |
| CRUD | `/api/collections/:id/storage-units/` | Yes | Binders, boxes, etc. |
| CRUD | `/api/collections/:id/instances/` | Yes | Owned cards |
| GET | `/api/games/`, `/api/sets/`, `/api/cards/` | Yes | Card catalog |

## Documentation

- [Design document](docs/design.md) — purpose, domain model, features, and deployment strategy

## Development without Docker

If you prefer running services natively:

**Backend** — requires Python 3.12+, PostgreSQL running locally:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export POSTGRES_HOST=localhost  # plus other vars from .env.example
python manage.py makemigrations users catalog collections
python manage.py migrate
python manage.py runserver
```

**Frontend** — requires Node 20+:

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_PROXY_TARGET=http://localhost:8000` so Vite proxies `/api` to Django.
