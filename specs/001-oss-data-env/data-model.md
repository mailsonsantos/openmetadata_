# Data Model: OpenMetadata Sandbox

This document outlines the conceptual data model and physical schemas for the synthetic data ingested into the OpenMetadata sandbox.

## 1. Physical Storage Architecture

- **S3 Bucket**: `s3a://datalake`
- **Hive Database / Trino Schema**: `sandbox`
- **Table Name**: `financial_transactions`

## 2. Table: `financial_transactions`

Stores synthetic financial transaction records.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `transaction_id` | `STRING` | Unique identifier for the transaction (UUID) |
| `account_id` | `STRING` | Identifier for the user account |
| `amount` | `DOUBLE` | Transaction amount |
| `currency` | `STRING` | Currency code (e.g., USD, EUR, BRL) |
| `transaction_date` | `TIMESTAMP` | Timestamp when the transaction occurred |
| `status` | `STRING` | Status of the transaction (e.g., COMPLETED, PENDING, FAILED) |
| `merchant_name` | `STRING` | Name of the merchant |

## 3. Metadata Entities in OpenMetadata

Once ingested, the following entities will be represented in OpenMetadata:

- **Database Service**: `local_trino`
- **Database**: `hive` (default Trino catalog name for the Hive connector)
- **Schema**: `sandbox`
- **Table**: `financial_transactions`
- **Lineage**: Spark Script -> `financial_transactions` table (if supported via Spark Lineage integration or manually annotated via API).
