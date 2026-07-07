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
