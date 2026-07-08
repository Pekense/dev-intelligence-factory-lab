#!/usr/bin/env bash

set -e

echo "Starting DEV Intelligence Factory local pipeline..."

echo ""
echo "1. Validating DEV environment files..."
./scripts/validate-env.sh

echo ""
echo "2. Running backend tests..."
cd backend
source .venv/bin/activate
export PYTHONPATH=$PWD
pytest
cd ..

echo ""
echo "3. Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo ""
echo "4. Validating Terraform..."
cd infrastructure
terraform fmt -check
terraform validate
terraform plan
cd ..

echo ""
echo "Local pipeline completed successfully."
