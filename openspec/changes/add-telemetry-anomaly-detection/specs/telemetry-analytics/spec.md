## ADDED Requirements
### Requirement: Telemetry Anomaly Detection
The system SHALL detect anomalies in device telemetry using per-device baselines and configurable sensitivity per metric.

#### Scenario: Flag high-severity anomaly
- **WHEN** a metric deviates from its rolling baseline beyond the configured threshold and the minimum data window is satisfied
- **THEN** the system records an anomaly event with device, metric, severity, timestamp, and summary statistics

#### Scenario: Avoid duplicate anomalies
- **WHEN** repeated out-of-range readings occur within the same active anomaly window
- **THEN** the system SHALL update the existing open anomaly instead of creating duplicates, preserving first/last seen timestamps

### Requirement: Anomaly Notification Routing
The system SHALL notify subscribers about anomalies according to channel preferences and throttle rules.

#### Scenario: Send notification
- **WHEN** a new high or critical anomaly is recorded for a device with notifications enabled
- **THEN** the system sends an alert via the configured channels (email/webhook) including device, metric, severity, and event time

#### Scenario: Throttle noisy devices
- **WHEN** a device produces multiple anomalies within the configured throttle window
- **THEN** the system suppresses repeat notifications until the window resets while still recording the underlying anomaly events

### Requirement: Anomaly Query API
The system SHALL expose API endpoints to query anomalies by device, metric, severity, and time range.

#### Scenario: Paginated query
- **WHEN** a client requests anomalies for a device with filters and a time range
- **THEN** the API returns a paginated list of anomaly records with total counts and next-page cursors
