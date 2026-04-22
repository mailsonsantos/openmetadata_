# Infrastructure Contracts

As this project focuses on deploying an infrastructure sandbox, the "contracts" refer to the service endpoints and configuration boundaries between components.

## Service Endpoints (Docker Compose Network)

| Service | Internal Hostname | Port | Purpose |
| :--- | :--- | :--- | :--- |
| **MinIO** | `minio` | `9000` | S3 API endpoint for Spark and Trino |
| **MinIO Console** | `minio` | `9001` | Web UI for object storage management |
| **Hive Metastore** | `hive-metastore`| `9083` | Thrift URI for Spark and Trino schema registry |
| **Trino** | `trino` | `8080` | JDBC endpoint for OpenMetadata and queries |
| **OpenMetadata Server** | `openmetadata-server`| `8585` | Main UI and API for the catalog |
| **Spark App** | `spark-app` | N/A | Ephemeral container for data generation |

## Trino Catalog Contract (`hive` catalog)

Trino is configured to expose MinIO data using the Hive Metastore.
The contract for Trino's `hive` catalog is defined as:

- **Type**: `hive`
- **URI**: `thrift://hive-metastore:9083`
- **S3 Endpoint**: `http://minio:9000`
- **Authentication**: Access Key / Secret Key provided via environment.
