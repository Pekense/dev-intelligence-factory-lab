CREATE TABLE IF NOT EXISTS shipments (
    id SERIAL PRIMARY KEY,
    client VARCHAR(120) NOT NULL,
    destination VARCHAR(120) NOT NULL,
    location VARCHAR(120) NOT NULL,
    status VARCHAR(50) NOT NULL,
    transport_service VARCHAR(120) NOT NULL,
    eta TIMESTAMP NOT NULL,
    temperature_current NUMERIC(5,2),
    alert_status VARCHAR(50),
    last_logistic_event VARCHAR(255)
);

INSERT INTO shipments (
    client,
    destination,
    location,
    status,
    transport_service,
    eta,
    temperature_current,
    alert_status,
    last_logistic_event
) VALUES
(
    'ACME Pharma',
    'Madrid',
    'Zaragoza Hub',
    'IN_TRANSIT',
    'Cold Chain Express',
    '2026-07-08 18:00:00',
    4.5,
    'NORMAL',
    'Shipment departed from Zaragoza Hub'
),
(
    'Global Retail',
    'Barcelona',
    'Valencia Port',
    'PENDING',
    'Maritime Standard',
    '2026-07-09 09:30:00',
    18.2,
    'NORMAL',
    'Container registered at port'
);

CREATE TABLE IF NOT EXISTS ai_change_requests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(180) NOT NULL,
    requester VARCHAR(120) NOT NULL,
    request_type VARCHAR(50) NOT NULL,
    priority VARCHAR(30) NOT NULL DEFAULT 'MEDIUM',
    description TEXT NOT NULL,
    constraints TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'NEW',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO ai_change_requests (
    title,
    requester,
    request_type,
    priority,
    description,
    constraints,
    status
)
SELECT
    'Dashboard branding and shipment location visibility',
    'CIO',
    'FUNCTIONAL',
    'HIGH',
    'Add a corporate identity placeholder and make the current shipment location easier to identify.',
    'DEV only. No real logos. No secrets. No production. Pipeline and human review required.',
    'NEW'
WHERE NOT EXISTS (
    SELECT 1
    FROM ai_change_requests
    WHERE title = 'Dashboard branding and shipment location visibility'
);
