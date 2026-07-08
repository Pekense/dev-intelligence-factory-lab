#!/usr/bin/env bash

set -e

QUEUE_URL="http://sqs.eu-west-1.localhost.localstack.cloud:4566/000000000000/temperature-events-dev"

SHIPMENT_ID="${1:-1}"
TEMPERATURE="${2:-7.8}"
STATUS="${3:-WARNING}"
SOURCE="temperature-sensor-dev"

MESSAGE_BODY=$(cat <<JSON
{
  "shipment_id": ${SHIPMENT_ID},
  "temperature": ${TEMPERATURE},
  "status": "${STATUS}",
  "source": "${SOURCE}"
}
JSON
)

echo "Sending temperature event to LocalStack SQS..."
echo "$MESSAGE_BODY"

docker exec dif-localstack awslocal sqs send-message \
  --queue-url "$QUEUE_URL" \
  --message-body "$MESSAGE_BODY"

echo "Temperature event sent successfully."
