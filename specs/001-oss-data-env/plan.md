# Implementation Plan: Ambiente Open-Source para OpenMetadata

**Branch**: `001-oss-data-env` | **Date**: 2026-04-22 | **Spec**: specs/001-oss-data-env/spec.md
**Input**: Feature specification from `/specs/001-oss-data-env/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Deploy a fully functional local open-source data environment orchestrating MinIO, Hive Metastore, Trino, and OpenMetadata via Docker Compose, along with a PySpark script for synthetic data generation to support end-to-end data lineage testing.

## Technical Context

**Language/Version**: Docker Compose, Python 3.11 (PySpark)
**Primary Dependencies**: MinIO, Hive Metastore, Trino, OpenMetadata, PySpark
**Storage**: MinIO (Object Storage) & Hive Metastore Backend (PostgreSQL)
**Testing**: Docker Healthchecks, Trino Queries
**Target Platform**: Local Docker Environment
**Project Type**: Sandbox / Data Environment
**Performance Goals**: Startup within 5 minutes
**Constraints**: 8GB-12GB free RAM required
**Scale/Scope**: 1000+ rows synthetic data, end-to-end integration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Constitution is generic. No violations detected in deploying a containerized data sandbox.

## Project Structure

### Documentation (this feature)

```text
specs/001-oss-data-env/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
docker/
├── docker-compose.yml
├── init-minio/
│   └── setup.sh
├── init-trino/
│   └── catalog/
│       └── minio.properties
└── openmetadata/
    └── .env

src/
├── spark/
│   ├── generate_synthetic_data.py
│   └── requirements.txt
```

**Structure Decision**: A `docker` folder for infrastructure configurations and initialization scripts, and a `src/spark` folder for the PySpark synthetic data generation script.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |
