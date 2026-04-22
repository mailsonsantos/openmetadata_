# Feature Specification: Ambiente Open-Source para OpenMetadata

**Feature Branch**: `001-oss-data-env`  
**Created**: 2026-04-22  
**Status**: Draft  
**Input**: User description: "Ambiente Open-Source para OpenMetadata com Spark, Trino (Athena-like) e MinIO (S3-like). Atue como Engenheiro de Dados. Como o LocalStack Community não suporta Athena/Glue, monte a estrutura usando componentes open-source equivalentes."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Environment Deployment (Priority: P1)

As a Data Engineer, I want to deploy all necessary services (MinIO, Hive Metastore, Trino, OpenMetadata) locally via Docker Compose, so that I have a fully functional open-source data environment.

**Why this priority**: Without the underlying infrastructure running, no further data engineering or cataloging tasks can be performed.

**Independent Test**: Can be fully tested by running `docker-compose up` and accessing the UIs/APIs for MinIO, Trino, and OpenMetadata to ensure they are healthy.

**Acceptance Scenarios**:

1. **Given** a machine with Docker, **When** I run the compose file, **Then** MinIO is accessible on the configured ports for API and Console.
2. **Given** the environment is starting, **When** Hive Metastore and Trino initialize, **Then** Trino successfully connects to the Hive Metastore backend.
3. **Given** all backend services are running, **When** OpenMetadata starts, **Then** it can successfully connect to Trino.

---

### User Story 2 - Initial Data Setup (Priority: P1)

As a Data Engineer, I want to run setup scripts to create the initial buckets in MinIO and schemas/tables in Trino, so that the environment is ready to receive data.

**Why this priority**: The structure (buckets, schemas) must exist before the Spark simulation or OpenMetadata ingestion can occur.

**Independent Test**: Can be fully tested by running the setup scripts and querying Trino/MinIO CLI to verify the existence of the created assets.

**Acceptance Scenarios**:

1. **Given** MinIO is running, **When** I execute the MinIO setup script, **Then** the required buckets are created.
2. **Given** Trino and Hive are running, **When** I execute the Trino setup script, **Then** the specified schemas and tables are visible in the Hive Metastore.

---

### User Story 3 - Synthetic Data Ingestion via Spark (Priority: P2)

As a Data Engineer, I want to run a Spark Python script that generates Parquet data, saves it to MinIO, and registers the table in Hive Metastore, so that I have sample data to catalog.

**Why this priority**: Populating the environment with synthetic data is necessary to validate OpenMetadata's capabilities.

**Independent Test**: Can be fully tested by running the Python script and verifying the parquet files in MinIO and the table registration in Trino.

**Acceptance Scenarios**:

1. **Given** the data environment is set up, **When** I run the Spark simulator, **Then** it successfully connects to MinIO.
2. **Given** the Spark job completes, **When** I query Trino, **Then** I can see the new table and its data.

---

### Edge Cases

- What happens when a service (e.g., Hive Metastore) fails to start before Trino? (Need proper dependencies/wait conditions in Docker Compose).
- How does the system handle running the setup scripts multiple times? (Should be idempotent).
- What happens if the Spark script encounters connection timeouts with MinIO?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a deployment configuration that provisions MinIO, Hive Metastore, Trino, and OpenMetadata locally.
- **FR-002**: System MUST configure Trino with a connector to read from MinIO and manage metadata in Hive Metastore.
- **FR-003**: System MUST provide an automated way to create specific MinIO buckets.
- **FR-004**: System MUST provide an automated way to initialize schemas and tables in Trino.
- **FR-005**: System MUST provide a Spark script configured to write data to MinIO.
- **FR-006**: System MUST ensure the Spark script registers its output table in the Hive Metastore.
- **FR-007**: System MUST configure OpenMetadata services to extract metadata from Trino and MinIO.

### Key Entities

- **Storage Bucket**: The logical storage container for data files.
- **Data Table**: The logical representation of the data stored in the bucket, managed by the metastore.
- **Compute Session**: The process that writes data to storage.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The entire data environment starts up and becomes healthy within 5 minutes on a standard developer machine.
- **SC-002**: Setup scripts run without manual intervention.
- **SC-003**: The Spark script successfully generates and writes at least 1000 rows of synthetic data.
- **SC-004**: OpenMetadata successfully connects to Trino and MinIO, mapping 100% of the schemas and tables created.

## Assumptions

- Users have a containerization engine installed locally.
- Users have an environment capable of running the Spark script.
- The host machine has sufficient RAM (at least 8GB-12GB free) to run all these services concurrently.
- Basic, non-production authentication (or default credentials) is sufficient for this sandbox environment.
