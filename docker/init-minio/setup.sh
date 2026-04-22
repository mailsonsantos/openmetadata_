#!/bin/sh
set -e

MC_ALIAS="local"
MINIO_URL="http://minio:9000"
ACCESS_KEY="${MINIO_ROOT_USER:-minioadmin}"
SECRET_KEY="${MINIO_ROOT_PASSWORD:-minioadmin}"

echo "Waiting for MinIO to be ready..."
until mc alias set "$MC_ALIAS" "$MINIO_URL" "$ACCESS_KEY" "$SECRET_KEY"; do
  echo "MinIO not ready yet, retrying in 3s..."
  sleep 3
done

echo "Creating 'datalake' bucket..."
mc mb --ignore-existing "$MC_ALIAS/datalake"

echo "Setting public read policy on 'datalake' bucket..."
mc anonymous set download "$MC_ALIAS/datalake"

echo "MinIO setup complete."
