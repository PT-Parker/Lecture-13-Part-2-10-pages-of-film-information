# Change: Add telemetry anomaly detection and alerting

## Why
- Operators currently rely on manual dashboard checks to spot bad device behavior, leading to slow incident response and missed issues.

## What Changes
- Add analytics job to detect anomalies on telemetry streams using per-device baselines and configurable sensitivity.
- Persist anomaly events with severity, metric, device, and timestamps; expose them through API endpoints and UI lists.
- Send notifications (email/webhook) for high-severity anomalies with per-device/channel preferences and throttling.
- Add configuration for per-device thresholds and a small UI surface for anomaly visibility.

## Impact
- Affected specs: telemetry-analytics
- Affected code: analytics jobs, ingestion validation, alerting/notification services, API layer, dashboard UI
