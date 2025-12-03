## 1. Implementation
- [ ] 1.1 Define anomaly data model (table, indexes, status lifecycle) and migrations.
- [ ] 1.2 Add analytics job to compute anomalies from telemetry (rolling baseline/z-score), idempotent per device/metric window.
- [ ] 1.3 Expose API endpoints to list anomalies by device/metric/severity/time range with pagination.
- [ ] 1.4 Implement notification routing (email/webhook) with per-device preferences and throttle windows.
- [ ] 1.5 Add UI surface (dashboard card + detail list) for recent anomalies with filters.
- [ ] 1.6 Add tests: Pytest for analytics + API, Vitest/RTL for UI, and a smoke E2E for alert dispatch.
