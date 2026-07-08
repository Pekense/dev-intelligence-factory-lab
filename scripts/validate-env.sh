#!/usr/bin/env bash

set -e

BACKEND_ENV_FILE="config/backend.dev.env"
FRONTEND_ENV_FILE="config/frontend.dev.env"

echo "Validating DEV environment files..."

if [ ! -f "$BACKEND_ENV_FILE" ]; then
  echo "Missing backend environment file: $BACKEND_ENV_FILE"
  exit 1
fi

if [ ! -f "$FRONTEND_ENV_FILE" ]; then
  echo "Missing frontend environment file: $FRONTEND_ENV_FILE"
  exit 1
fi

required_backend_vars=(
  "ENVIRONMENT"
  "DATABASE_URL"
  "DASHBOARD_REFRESH_INTERVAL_SECONDS"
)

required_frontend_vars=(
  "VITE_API_BASE_URL"
  "VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS"
)

for var in "${required_backend_vars[@]}"; do
  if ! grep -q "^${var}=" "$BACKEND_ENV_FILE"; then
    echo "Missing backend variable: $var"
    exit 1
  fi
done

for var in "${required_frontend_vars[@]}"; do
  if ! grep -q "^${var}=" "$FRONTEND_ENV_FILE"; then
    echo "Missing frontend variable: $var"
    exit 1
  fi
done

backend_refresh_interval=$(grep "^DASHBOARD_REFRESH_INTERVAL_SECONDS=" "$BACKEND_ENV_FILE" | cut -d "=" -f2)
frontend_refresh_interval=$(grep "^VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS=" "$FRONTEND_ENV_FILE" | cut -d "=" -f2)

if ! [[ "$backend_refresh_interval" =~ ^[0-9]+$ ]]; then
  echo "DASHBOARD_REFRESH_INTERVAL_SECONDS must be numeric"
  exit 1
fi

if ! [[ "$frontend_refresh_interval" =~ ^[0-9]+$ ]]; then
  echo "VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS must be numeric"
  exit 1
fi

if [ "$backend_refresh_interval" -lt 10 ]; then
  echo "DASHBOARD_REFRESH_INTERVAL_SECONDS must be at least 10 seconds"
  exit 1
fi

if [ "$frontend_refresh_interval" -lt 10 ]; then
  echo "VITE_DASHBOARD_REFRESH_INTERVAL_SECONDS must be at least 10 seconds"
  exit 1
fi

echo "DEV environment validation passed."
