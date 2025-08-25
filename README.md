# SaaSNoteApp

A multi‑service (frontend + backend) SaaS note‑taking and knowledge organization platform.  
Frontend is a React + TypeScript + Vite SPA. Backend services are Python based: Django (core platform, auth, billing, admin) and FastAPI (high‑performance notes & realtime APIs). PostgreSQL provides persistence; Redis powers caching, rate limiting, websockets pub/sub, and background jobs. Everything is containerized with Docker for reproducible environments.

> Replace or prune any placeholder sections marked with 🔧 once confirmed.

---

## Table of Contents
1. Purpose & Vision  
2. Feature Overview  
3. Architecture  
4. Tech Stack  
5. Repository / Directory Structure  
6. Quick Start (TL;DR)  
7. Detailed Setup  
8. Environment Variables  
9. Running Services (Dev / Docker)  
10. Database & Migrations  
11. Caching & Queues  
12. API Overview & Examples  
13. Frontend Usage & Scripts  
14. Authentication & Authorization  
15. Background Tasks  
16. Deployment Guidelines  
17. Logging, Monitoring & Observability  
18. Testing Strategy  
19. Performance Considerations  
20. Security Practices  
21. Troubleshooting  
22. Roadmap  
23. Contributing  
24. License  
25. FAQ  
26. Acknowledgements

---

## 1. Purpose & Vision
SaaSNoteApp helps individuals and teams:
- Capture rich, structured, and searchable notes quickly.
- Organize with tags, folders, backlinks, and full‑text search.
- Collaborate (planned: shared workspaces, comments, presence).
- Operate as a multi‑tenant SaaS with subscription tiers.
- Integrate with external services (webhooks, export, AI—optional).

🔧 Add unique differentiators (e.g., AI semantic clustering, offline-first sync).

---

## 2. Feature Overview
| Category | Implemented / Planned | Notes |
|----------|-----------------------|-------|
| Rich Editing | Markdown, code blocks, attachments | React editor component |
| Organization | Folders, tags, pin/favorites | Tag search via Postgres GIN |
| Search | Full-text + filters | Django / FastAPI endpoints |
| Version History | Planned | Postgres note_revisions table |
| Realtime Collab | Planned (Redis pub/sub) | Websocket events |
| Multi-Tenancy | Tenant scoping per user/org | Always include tenant_id |
| Auth | JWT + refresh / session cookies | Django primary auth authority |
| Billing | Planned (Stripe) | Webhooks to Django |
| Export / Import | Markdown download | Future: bulk ZIP |
| API Tokens | Personal access tokens | Scope: read/write |
| Dark Mode | Implemented (CSS variables) | Persist theme in localStorage |
| Rate Limiting | Redis sliding window | Per IP + user ID |

Move not-yet-built items to Roadmap.

---

## 3. Architecture

```
                    ┌────────────────────────────┐
                    │        React (Vite)        │
                    │  TypeScript SPA (port 5173)│
                    └─────────────┬──────────────┘
                                  │ HTTPS (REST / WebSocket)
            ┌─────────────────────┴─────────────────────┐
            │                                           │
┌──────────────────────────────┐          ┌───────────────────────────────┐
│ Django Service (core)        │          │ FastAPI Service (notes API)   │
│ - Auth, tenants, billing     │  RPC/    │ - CRUD notes, search, RT ws   │
│ - Admin panel, user mgmt     │  REST    │ - High throughput endpoints   │
└───────────┬──────────────────┘          └───────────┬───────────────────┘
            │                                         │
            │ Shared                                  │
            │ Models (some via internal API)          │
            │                                         │
        ┌───▼─────────────────────────────────────────▼───┐
        │                PostgreSQL (primary)              │
        │  users / tenants / notes / tags / revisions      │
        └───────────┬───────────────────────┬─────────────┘
                    │                       │
               ┌────▼─────┐           ┌─────▼──────┐
               │  Redis   │           │  Object    │
               │ cache +  │           │ Storage    │
               │ rate limit│          │ (S3/minio) │
               └────┬─────┘           └────────────┘
                    │
               Background Workers (RQ / custom async tasks)
```

---

## 4. Tech Stack
- Frontend: React 18, TypeScript, Vite, React Query (data fetching), TailwindCSS (or CSS Modules)
- Backend Core: Django 5.x (REST framework optional), Django Admin
- Backend High-Perf: FastAPI (uvicorn), Pydantic for schemas
- DB: PostgreSQL (jsonb + GIN indexes)
- Cache / Queue / PubSub: Redis
- Messaging / Realtime: WebSockets (FastAPI) + Redis channels
- Containerization: Docker & docker compose
- Testing: pytest (backend), vitest / jest + testing-library (frontend)
- Linting: ruff / mypy (backend), ESLint / Prettier / TypeScript (frontend)
- CI: GitHub Actions
- Optional AI: External API via FastAPI service wrapper (🔧 if used)

---

## 5. Repository / Directory Structure (Example)

```
.
├─ frontend/                # React + Vite app
│  ├─ src/
│  │  ├─ components/
│  │  ├─ features/notes/
│  │  ├─ hooks/
│  │  ├─ lib/
│  │  ├─ styles/
│  │  └─ main.tsx
│  ├─ index.html
│  └─ vite.config.ts
├─ services/
│  ├─ django_core/
│  │  ├─ manage.py
│  │  ├─ core/ (settings, urls)
│  │  ├─ accounts/ (auth, tenants)
│  │  ├─ billing/
│  │  ├─ api/ (DRF endpoints if used)
│  │  └─ tests/
│  └─ fastapi_notes/
│     ├─ app/
│     │  ├─ main.py
│     │  ├─ api/
│     │  ├─ models/
│     │  ├─ schemas/
│     │  ├─ services/
│     │  └─ ws/
│     └─ tests/
├─ migrations/ (if centralized) or individual per service
├─ scripts/
├─ infra/
│  ├─ docker/
│  │  ├─ frontend.Dockerfile
│  │  ├─ django.Dockerfile
│  │  ├─ fastapi.Dockerfile
│  │  └─ worker.Dockerfile
│  └─ compose/
│     └─ docker-compose.dev.yml
├─ docs/
│  ├─ architecture.md
│  └─ api-reference.md
├─ .env.example
└─ README.md
```

Adjust to actual repo layout.

---

## 6. Quick Start (TL;DR)

```bash
# Clone
git clone https://github.com/nhan4013/SaaSNoteApp.git
cd SaaSNoteApp

# Environment
cp .env.example .env

# Docker (recommended for first run)
docker compose -f infra/compose/docker-compose.dev.yml up --build

# Frontend (if running standalone)
cd frontend && npm install && npm run dev
```

Visit: http://localhost:5173 (frontend)  
API (FastAPI): http://localhost:8001/docs  
Django Admin: http://localhost:8000/admin

---

## 7. Detailed Setup

### Prerequisites
- Node.js >= 18
- Python >= 3.11
- PostgreSQL >= 14
- Redis >= 6
- Docker & docker compose (optional but recommended)
- Make (optional convenience)

### Manual (Non-Docker) Backend Boot
```bash
# Django
cd services/django_core
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000

# FastAPI
cd ../fastapi_notes
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 8. Environment Variables

`.env.example` (extract or adapt):

| Variable | Service | Description | Example |
|----------|---------|-------------|---------|
| POSTGRES_HOST | all | DB host | localhost |
| POSTGRES_PORT | all | DB port | 5432 |
| POSTGRES_DB | all | Database name | saasnote |
| POSTGRES_USER | all | DB user | devuser |
| POSTGRES_PASSWORD | all | DB password | devpass |
| DATABASE_URL | django/fastapi | Full DSN | postgres://devuser:devpass@localhost:5432/saasnote |
| REDIS_URL | all | Redis connection | redis://localhost:6379/0 |
| SECRET_KEY | django | Django secret | (generated) |
| DJANGO_DEBUG | django | Debug flag | True |
| ALLOWED_HOSTS | django | Host whitelist | localhost,127.0.0.1 |
| CORS_ORIGINS | backend | Frontend origins | http://localhost:5173 |
| JWT_SECRET | fastapi | JWT signing secret | (generated) |
| JWT_EXP_MINUTES | fastapi | Access token TTL | 30 |
| REFRESH_EXP_DAYS | fastapi | Refresh token TTL | 7 |
| NOTE_MAX_SIZE_KB | fastapi | Guard large notes | 256 |
| RATE_LIMIT_WINDOW | fastapi | Seconds | 60 |
| RATE_LIMIT_MAX | fastapi | Requests per window | 120 |
| STRIPE_SECRET_KEY | django | Billing (🔧 optional) | sk_test_xxx |
| STRIPE_WEBHOOK_SECRET | django | Webhook verify | whsec_xxx |
| STORAGE_BUCKET | backend | Attachments bucket | notes-bucket |
| STORAGE_ENDPOINT | backend | S3/minio endpoint | http://minio:9000 |
| STORAGE_ACCESS_KEY | backend | Storage key | dev |
| STORAGE_SECRET_KEY | backend | Storage secret | dev |
| FRONTEND_BASE_URL | frontend | Used for OAuth redirects | http://localhost:5173 |
| SENTRY_DSN | all | Error tracking | https://... |
| LOG_LEVEL | all | logging level | info |

Mark required vs optional in the example file.

---

## 9. Running Services (Dev / Docker)

### Docker Compose (Dev)
`infra/compose/docker-compose.dev.yml` (conceptual):
- postgres
- redis
- django_core (depends on postgres, redis)
- fastapi_notes (depends on postgres, redis)
- frontend (dev server)
- worker (RQ / custom tasks)
- minio (optional for object storage)

Start:
```bash
docker compose -f infra/compose/docker-compose.dev.yml up --build
```

Rebuild single service:
```bash
docker compose -f infra/compose/docker-compose.dev.yml build fastapi_notes
```

Run migrations (Django inside container):
```bash
docker compose exec django_core python manage.py migrate
```

---

## 10. Database & Migrations

### Django (primary migrations)
```bash
python manage.py makemigrations
python manage.py migrate
```

### FastAPI Models
Option A: Use SQLAlchemy models in FastAPI referencing same database; manage migrations with Alembic.
```bash
alembic revision --autogenerate -m "add note revisions"
alembic upgrade head
```

Ensure consistent ownership: Django owns canonical models OR both coordinate on a shared schema segment. Avoid divergent migrations. Consider one migration tool (Alembic) for FastAPI-specific tables only.

Indexes (example):
```sql
CREATE INDEX IF NOT EXISTS idx_notes_tsv ON notes USING GIN(to_tsvector('english', title || ' ' || content));
CREATE INDEX IF NOT EXISTS idx_tags_note_id ON note_tags(note_id);
```

---

## 11. Caching & Queues
- Redis keys:
  - `note:{id}` single note cache
  - `user_session:{token}` authentication
  - `rl:{user_or_ip}:{window}` rate limiting
- TTL Strategy:
  - Notes: 60s (soft cache)
  - Sessions: align with JWT expiry
- Background Jobs (RQ / custom): indexing, sending emails, generating exports.

---

## 12. API Overview & Examples

### Auth (FastAPI or Django token endpoint)
```http
POST /api/auth/login
Content-Type: application/json
{
  "email": "user@example.com",
  "password": "secret"
}
```
Response:
```json
{
  "access_token": "jwt...",
  "refresh_token": "jwt_r...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Refresh
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

### Create Note
```http
POST /api/notes
Authorization: Bearer <access_token>
Content-Type: application/json
{
  "title": "Meeting Notes",
  "content": "## Agenda\n- Point A",
  "tags": ["work","2025"]
}
```

Response minimal:
```json
{ "id": "note_123", "title": "Meeting Notes", "created_at": "2025-08-25T10:00:00Z" }
```

### Search
```http
GET /api/notes?query=meeting&limit=20
Authorization: Bearer <access_token>
```

### Realtime WebSocket
```
wss://localhost:8001/ws/notes/note_123?token=<access_token>
```
Message shape:
```json
{
  "type": "op",
  "op": {"range":[10,14],"text":"Action Item"}
}
```

### Error Format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Title required",
    "details": {"field":"title"}
  }
}
```

Document complete schemas in `docs/api-reference.md`.

---

## 13. Frontend Usage & Scripts
Scripts (package.json):
- `dev` Vite dev server
- `build` production build
- `preview` preview build
- `lint` ESLint
- `typecheck` tsc --noEmit
- `test` vitest run

State management: React Query for server cache + context for auth tokens.

Environment variables (frontend):
- `VITE_API_BASE_URL`
- `VITE_WS_BASE_URL`
- `VITE_SENTRY_DSN` (optional)
(Define in `frontend/.env`)

---

## 14. Authentication & Authorization
Flow:
1. User login -> receives access + refresh tokens.
2. Access token short-lived (e.g., 30 min), refresh extends session.
3. Frontend stores access token in memory, refresh in httpOnly cookie (recommended) or secure storage.
4. Multi-tenancy: every note query is scoped: `SELECT * FROM notes WHERE tenant_id = :tenant AND id = :id;`
5. Roles: `owner`, `admin`, `member`, `viewer` (🔧 finalize). Implement decorator / dependency that enforces role on endpoint.

---

## 15. Background Tasks
Potential tasks:
- `index_note_content(note_id)`
- `generate_note_export(note_id, format)`
- `send_welcome_email(user_id)`
- `purge_deleted_notes()`
Queue Reliability:
- Set max retries (e.g., 3) with exponential backoff.
- Dead-letter list key: `dq:failed`.

---

## 16. Deployment Guidelines
Options:
- Frontend: Static deploy (Netlify, Vercel) or served via Nginx container.
- Backends: Docker images on AWS ECS, Fly.io, Render, or Kubernetes cluster.
- DB: Managed Postgres (RDS, Supabase, Neon).
- Redis: Managed (Upstash, Redis Cloud).
- Object storage: S3 or R2.

Build & push example:
```bash
docker build -f infra/docker/django.Dockerfile -t registry/app-django:sha-<gitsha> .
docker push registry/app-django:sha-<gitsha>
```

Run migrations before flipping traffic:
```bash
python manage.py migrate --noinput
alembic upgrade head
```

Zero-downtime strategy: rolling update with health endpoints `/health` (FastAPI) & `/healthz` (Django).

---

## 17. Logging, Monitoring & Observability
- Structured logs (JSON) with `timestamp`, `service`, `trace_id`.
- Correlate request ID across Django and FastAPI via header `X-Request-ID`.
- Metrics (Prometheus):
  - `http_requests_total{service,route,status}`
  - `db_query_duration_seconds`
  - `cache_hit_ratio`
- Tracing: OpenTelemetry exporters to Jaeger or Tempo.
- Alerts: 5xx rate > threshold, latency p95 > 800ms, error spikes.

---

## 18. Testing Strategy
Backend:
- Unit (pure util, services)
- API contract tests (pytest + httpx)
- DB integration (transaction rollback fixture)
Frontend:
- Component tests (testing-library)
- Hooks tests (React Testing Library + vitest)
- E2E (Playwright or Cypress) against docker-compose stack

Commands:
```bash
pytest -q
npm run test
```
Coverage:
```bash
pytest --cov=services
vitest run --coverage
```

---

## 19. Performance Considerations
- Use `select_related` / `prefetch_related` in Django.
- FastAPI endpoints rely on async DB driver (asyncpg via SQLAlchemy 2).
- Redis caching for list endpoints: Key invalidation on note mutation.
- Rate limit heavy endpoints (search).
- Debounced client-side autosave (e.g., 800ms after last keystroke).
- GZIP / Brotli compression at reverse proxy.
- Database indexes maintained (monitor bloat).

---

## 20. Security Practices
- Secure headers (CSP, X-Frame-Options, X-Content-Type-Options).
- CSRF: Django forms & cookie session; API endpoints use JWT (no CSRF).
- Input validation: Pydantic (FastAPI), DRF serializers or custom clean methods (Django).
- XSS: Sanitize user HTML; allowlist markdown conversions.
- Secrets: Never commit `.env`; use vault or platform secrets.
- Password storage: Django PBKDF2 or argon2 (preferred).
- Brute force: Rate limit login by IP + username combination.
- Multi-Tenancy: Always filter by `tenant_id`; enforce in model managers or query dependencies.

---

## 21. Troubleshooting

| Problem | Symptom | Fix |
|---------|---------|-----|
| DB connection refused | Startup crash / ECONNREFUSED | Confirm POSTGRES_* vars & container dependency order |
| Django allowed hosts error | 400 Bad Request | Add host to `ALLOWED_HOSTS` |
| CORS errors | Browser console blocked | Update `CORS_ORIGINS` env; enable credentials if needed |
| Redis timeouts | Slow responses | Check network / increase connection pool size |
| JWT invalid / expired | 401 responses | Refresh token; verify system time sync (NTP) |
| WebSocket fails | 403 or close immediately | Verify token query param; check reverse proxy upgrade headers |
| Migrations conflict | Duplicate column errors | Rebase migrations; squash or generate new consistent branch |
| High memory usage | Container OOMKilled | Inspect query plans; add indexes; reduce cache objects |
| Note search slow | >500ms latency | Confirm GIN index; ANALYZE; avoid leading wildcard queries |
| Static assets 404 | Styles missing | Rebuild frontend; ensure correct public path configuration |
| Rate limit triggered | 429 responses | Increase window or optimize batching |

General Debug Steps:
1. `docker compose logs -f fastapi_notes`
2. Check health endpoints `/health` or `/healthz`.
3. Run `EXPLAIN ANALYZE` on slow SQL.
4. Use `redis-cli monitor` (temporarily) to inspect traffic.
5. Validate migrations in a clean DB snapshot.

---

## 22. Roadmap
- [ ] Realtime collaborative cursors & presence
- [ ] AI-assisted note summaries
- [ ] Offline-first sync + conflict resolution
- [ ] Role-based granular permissions (share link vs org)
- [ ] Public note publishing with custom slug
- [ ] Bulk import (Markdown ZIP)
- [ ] Billing integration (Stripe) with plan enforcement
- [ ] Mobile-focused UI enhancements
- [ ] Activity feed & audit logging

Link tasks to GitHub Issues once created.

---

## 23. Contributing
1. Fork & clone repository
2. Create branch:
   ```bash
   git checkout -b feat/<short-description>
   ```
3. Ensure passing tests & linters:
   ```bash
   ruff check .
   mypy services/fastapi_notes/app
   pytest
   npm run lint
   npm run test
   ```
4. Conventional Commit message:
   ```
   feat(notes): add bulk tagging endpoint
   ```
5. Open Pull Request including:
   - Summary & rationale
   - Screenshots (UI changes)
   - Migration impact
   - Rollback steps

Code Style:
- Python: ruff + black formatting (if enabled)
- Type safety: mypy (strict optional)
- JS/TS: ESLint + Prettier
- Keep functions readable (prefer < 75 LOC, low cyclomatic complexity)
- Add tests for new endpoints / components

---

## 24. License
🔧 Choose and state license (e.g., MIT, AGPL, proprietary).  
Example:
```
MIT License © 2025 Your Name
```

---

## 25. FAQ
| Question | Answer |
|----------|--------|
| Is there a free tier? | 🔧 Define limits (e.g., max notes / storage) |
| Can I self-host? | Yes (Docker compose provided) |
| How is data stored? | PostgreSQL; attachments in S3-compatible storage |
| Are notes encrypted? | At rest via provider; end-to-end encryption planned |
| API rate limits? | Default 120 req / 60s per user (configurable) |
| Data export? | Endpoint `/api/notes/export` (planned bulk) |

---

## 26. Acknowledgements
- Django, FastAPI, React, Vite, PostgreSQL, Redis communities
- Open-source libraries enabling rapid development
- Inspiration from tools like Notion, Obsidian, and others

---

## Next Steps
1. Replace placeholders & confirm feature status.
2. Add real diagrams (`docs/architecture.md`) & screenshots.
3. Flesh out `docs/api-reference.md`.
4. Publish Issues for each roadmap item.
5. Configure CI pipeline references in README badges.

---

Badges (Optional):
[![CI](https://img.shields.io/badge/ci-passing-success)](./) [![License](https://img.shields.io/badge/license-TBD-informational)](./)

Questions? Open a Discussion or Issue.

---
