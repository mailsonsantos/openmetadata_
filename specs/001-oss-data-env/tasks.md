---
description: "Task list for OpenMetadata Sandbox Environment implementation"
---

# Tasks: Ambiente Open-Source para OpenMetadata

**Input**: Design documents from `/specs/001-oss-data-env/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (`docker/`, `docker/init-minio/`, `docker/init-trino/catalog/`, `docker/openmetadata/`, `src/spark/`)
- [X] T002 [P] Configure environment variables in `docker/openmetadata/.env`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T003 Configure base `docker-compose.yml` with network definitions and shared volumes

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Environment Deployment (Priority: P1) 🎯 MVP

**Goal**: Deploy all necessary services (MinIO, Hive Metastore, Trino, OpenMetadata) locally via Docker Compose.

**Independent Test**: Can be fully tested by running `docker-compose up` and accessing the UIs/APIs for MinIO, Trino, and OpenMetadata to ensure they are healthy.

### Implementation for User Story 1

- [X] T004 [P] [US1] Add MinIO service configuration to `docker/docker-compose.yml`
- [X] T005 [P] [US1] Add Hive Metastore backend (PostgreSQL) and Metastore service to `docker/docker-compose.yml`
- [X] T006 [P] [US1] Create Trino catalog properties in `docker/init-trino/catalog/minio.properties`
- [X] T007 [US1] Add Trino service configuration to `docker/docker-compose.yml` (depends on Hive and MinIO)
- [X] T008 [US1] Add OpenMetadata services and dependencies to `docker/docker-compose.yml`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Initial Data Setup (Priority: P1)

**Goal**: Run setup scripts to create the initial buckets in MinIO and schemas/tables in Trino.

**Independent Test**: Can be fully tested by running the setup scripts and querying Trino/MinIO CLI to verify the existence of the created assets.

### Implementation for User Story 2

- [X] T009 [P] [US2] Create MinIO initialization script in `docker/init-minio/setup.sh` to create `datalake` bucket
- [X] T010 [US2] Add MinIO setup service (using `mc` client) to `docker/docker-compose.yml`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Synthetic Data Ingestion via Spark (Priority: P2)

**Goal**: Run a Spark Python script that generates Parquet data, saves it to MinIO, and registers the table in Hive Metastore.

**Independent Test**: Can be fully tested by running the Python script and verifying the parquet files in MinIO and the table registration in Trino.

### Implementation for User Story 3

- [X] T011 [P] [US3] Create Spark dependencies file in `src/spark/requirements.txt`
- [X] T012 [US3] Implement synthetic data generation script in `src/spark/generate_synthetic_data.py` (matching `financial_transactions` data model)
- [X] T013 [US3] Add Spark job runner service to `docker/docker-compose.yml`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T014 Validate environment startup sequence and wait conditions in `docker/docker-compose.yml`
- [ ] T015 Run quickstart tests per `specs/001-oss-data-env/quickstart.md`
- [ ] T016 Setup OpenMetadata ingestion pipeline manually via UI (or document steps) to verify cataloging

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 must be completed first as it provides the core infrastructure
  - US2 depends on US1 infrastructure
  - US3 depends on US2 bucket setup

### Parallel Opportunities

- Structure creation (T001) and `.env` creation (T002) can be done in parallel.
- Adding MinIO (T004), Hive (T005), and Trino properties (T006) can be done in parallel.
- MinIO initialization script (T009) and Spark requirements (T011) can be prepared in parallel before their respective dependent tasks.

---

## Parallel Example: User Story 1

```bash
# Prepare base configurations in parallel
Task: "Add MinIO service configuration to docker/docker-compose.yml"
Task: "Add Hive Metastore backend (PostgreSQL) and Metastore service to docker/docker-compose.yml"
Task: "Create Trino catalog properties in docker/init-trino/catalog/minio.properties"
```
