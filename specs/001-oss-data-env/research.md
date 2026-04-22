# Research & Technical Decisions: Ambiente Open-Source para OpenMetadata

## 1. Compatibility and Service Versions

**Decision**: Use recent stable versions for all services:
- MinIO: `RELEASE.2024-*`
- Hive Metastore: `3.1.3` (with PostgreSQL backend)
- Trino: `435+`
- OpenMetadata: `1.3.x` or latest stable `1.4.x`
- PySpark: `3.5.x` with Hadoop AWS 3.3.x

**Rationale**: These versions ensure compatibility with modern S3 APIs and the latest Trino Hive connectors. OpenMetadata 1.3+ has mature connectors for Trino.
**Alternatives considered**: Using older versions like Hive 2.x, but it may lack support for newer S3 authentication mechanisms required by MinIO.

## 2. Trino Catalog Configuration

**Decision**: Use the Trino `hive` connector configured with S3-compatible endpoints.
- `hive.metastore.uri`: Thrift URI of Hive Metastore.
- `hive.s3.endpoint`: MinIO URL.
- `hive.s3.aws-access-key` / `hive.s3.aws-secret-key`: MinIO credentials.
- `hive.s3.path-style-access=true`: Required for MinIO.

**Rationale**: The `hive` connector in Trino natively supports querying data in S3/MinIO while using Hive Metastore for schema definitions.
**Alternatives considered**: Iceberg connector, but Hive is simpler for a baseline Parquet-based sandbox and aligns well with standard Spark behavior.

## 3. Spark Synthetic Data Generation

**Decision**: PySpark will run in a separate container connected to the Docker Compose network, writing directly to MinIO (`s3a://...`) and saving as a table to Hive Metastore via thrift URI.

**Rationale**: Using a containerized Spark setup avoids requiring the user to have Java/Spark installed on their host machine, making the environment completely self-contained.
**Alternatives considered**: Running Spark locally on the host, which violates the requirement for a self-contained local environment.

## 4. OpenMetadata Integration

**Decision**: Configure the OpenMetadata Trino ingestion pipeline to point to the Trino coordinator. Trino acts as the query engine and schema registry proxy, allowing OpenMetadata to catalog tables, schemas, and columns automatically.

**Rationale**: OpenMetadata has a native connector for Trino that supports data profiling, lineage (if queries are run), and metadata extraction.
**Alternatives considered**: Pointing OpenMetadata directly to Hive Metastore, but querying via Trino is closer to an Athena-like architecture.
