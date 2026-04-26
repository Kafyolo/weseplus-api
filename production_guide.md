# WesePlus Backend Production Deployment Guide

Your backend is now structured for production hosting and live testing. This guide explains how to use the new setup.

## Key Changes
- **Process Manager**: Switched from Uvicorn (dev) to Gunicorn with Uvicorn workers. This provides better stability and handles multi-concurrency more efficiently.
- **Security**: CORS is now dynamic. You must define `ALLOWED_ORIGINS` in your `.env` file (e.g., `ALLOWED_ORIGINS=https://your-app.com,https://dashboard.weseplus.com`).
- **Database Migrations**: We have added **Alembic**. You can no longer rely on the app automatically creating tables on startup. This protects your production data during updates.
- **Docker**: A new `docker-compose.prod.yml` is provided which omits volume mounts for performance and security.

## How to Run in Production

### 1. Configure Environment
Create a `.env` file in the root directory (based on `.env.example`).
```bash
DATABASE_URL=postgresql://user:password@db:5432/weseplus
SECRET_KEY=generate-a-strong-random-key
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 2. Deploy with Docker
Run the production compose file:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### 3. Handle Database Migrations
Since `Base.metadata.create_all` is now disabled in `main.py`, you must use Alembic to manage your schema.

#### Generate Initial Migration (First time only)
If your database is empty, run:
```bash
# Enter the API container
docker exec -it weseplus_api_prod bash

# Generate the first migration based on your models
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to the database
alembic upgrade head
```

#### Making Schema Changes
Whenever you modify a file in `app/models/`, repeat the steps above to generate and apply a new revision.

## Local Development Still Works
You can still run the backend locally for development using the original `docker-compose.yml` (which uses volume mounts for hot-reloading) or by running:
```bash
# Note: You'll need to install dependencies first
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---
**WesePlus Production Ready Analysis & Implementation Completed.**
