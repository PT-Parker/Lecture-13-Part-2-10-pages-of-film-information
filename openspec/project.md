# Project Context

## Purpose
Build an IoT telemetry analysis platform that ingests device sensor data, cleans and aggregates it, and delivers dashboards and alerts for operations and classroom demos. Focus on fast turnaround from raw data to insight with minimal setup friction.

## Tech Stack
- Backend: Python 3.11 with FastAPI for APIs and ingestion services
- Data: PostgreSQL/TimescaleDB for time-series storage; S3-compatible object storage for raw files; Redis for lightweight job queues/caching
- Frontend: React + TypeScript (Vite) with a simple component library (Chakra UI) for dashboards
- Messaging/IoT: MQTT broker (Mosquitto/EMQX) for device telemetry ingestion
- Tooling: Docker Compose for local stacks; GitHub Actions for CI lint/test

## Project Conventions

### Code Style
- Python: Black + Ruff, type-hinted FastAPI/Pydantic models, async-first endpoints, dependency-injected services
- TypeScript/React: ESLint + Prettier, functional components with hooks, PascalCase components, camelCase props/vars, colocated CSS modules
- Config via `.env` for secrets and per-environment toggles; avoid committing secrets

### Architecture Patterns
- Layered flow: MQTT ingestion → parser/validator → persistence (Timescale) → analytics jobs → API → UI dashboards
- Repositories/services for data access; background jobs for batch analytics; WebSocket/SSE for live metric updates when needed
- Keep capabilities small and composable (ingestion, analytics, alerting, visualization)

### Testing Strategy
- Pytest for service/API layers with factory fixtures and DB containers
- Contract tests for MQTT payload shapes and validation rules
- Vitest + React Testing Library for UI; Playwright smoke tests for critical flows
- Require tests for new behavior and bug fixes; prefer lightweight fakes over heavy integration when possible

### Git Workflow
- Feature branches off `main`; short-lived and rebased regularly
- Conventional commits (`feat:`, `fix:`, `chore:`) with imperative mood
- PRs require at least one review; proposals (OpenSpec changes) must be approved before implementation
- Keep tasks.md in sync with work; close branches after merge

## Domain Context
- IoT devices emit timestamped telemetry (e.g., temperature, humidity, battery, status codes)
- Need near-real-time visibility plus historical trends; per-device metadata (location, firmware) is stored alongside readings
- Data quality matters: out-of-order timestamps, missing fields, and device clock drift are common

## Important Constraints
- Protect data in transit (TLS for MQTT/API) and at rest (disk encryption where available)
- Multi-tenant friendly: isolate device credentials and per-tenant data; avoid cross-tenant leaks in queries and caches
- Handle late-arriving/out-of-order telemetry; prefer idempotent ingestion
- Keep operational footprint small for classroom demos (Docker Compose-first)

## External Dependencies
- MQTT broker (Mosquitto/EMQX) for telemetry ingestion
- PostgreSQL/TimescaleDB instance for time-series and metadata
- Redis for background job queues and cache
- S3-compatible bucket for raw file dumps and backups
