# Quickstart: OpenMetadata Sandbox

This guide explains how to spin up the local data environment and run the synthetic data ingestion.

## Prerequisites
- Docker and Docker Compose installed.
- At least 8GB of free RAM.

## 1. Start the Environment
Run the following command from the repository root:
```bash
docker-compose up -d
```
Wait a few minutes for all services (MinIO, Hive Metastore, Trino, OpenMetadata) to become healthy.

## 2. Verify Services
- **MinIO Console**: `http://localhost:9001`
- **Trino UI**: `http://localhost:8080`
- **OpenMetadata UI**: `http://localhost:8585`

## 3. Generate Synthetic Data
Run the Spark job container to generate and ingest the data:
```bash
docker-compose run --rm spark-app
```
This script will:
1. Generate Parquet data in MinIO (`s3a://datalake/sandbox/financial_transactions`).
2. Register the table in the Hive Metastore.

## 4. Ingest Metadata into OpenMetadata
1. Log into OpenMetadata (`http://localhost:8585`).
2. Go to **Settings** > **Database Services** > **Add New Service**.
3. Select **Trino** and configure the connection to `trino:8080`.
4. Trigger an ingestion pipeline. The `sandbox.financial_transactions` table should appear in your catalog!
