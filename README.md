# Food Delivery Analytics Pipeline

An end-to-end data engineering portfolio project built to demonstrate production-grade pipeline development. The pipeline extracts raw food delivery data, loads it to Google BigQuery, and transforms it into business-ready analytics tables using dbt — all orchestrated by Apache Airflow running in Docker.

---

## Architecture

```
Python Extraction Script
  └─ Generates and loads raw data to BigQuery (raw_data dataset)
       ↓
Apache Airflow (Docker)
  └─ Orchestrates extract → transform pipeline on a daily schedule
       ↓
dbt Transformations (BigQuery)
  └─ Staging Layer    (views)   — clean and standardize raw data
  └─ Dimension Tables (tables)  — courier and zone lookup tables
  └─ Fact Table       (table)   — delivery transactions with full context
  └─ Mart Table       (table)   — aggregated courier performance metrics
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | Apache Airflow 2.10.4 |
| Containerization | Docker + Docker Compose |
| Transformation | dbt 1.11 |
| Data Warehouse | Google BigQuery |
| Extraction | Python 3.12 |
| Version Control | Git |

---

## Project Structure

```
food_delivery_analytics/
├── Dockerfile                        # Custom Airflow image with dbt installed
├── docker-compose.yaml               # Airflow stack (webserver, scheduler, postgres)
├── .env                              # Environment variables (not committed)
├── .gitignore
├── airflow/
│   └── dags/
│       └── food_delivery_pipeline.py # DAG definition
├── scripts/
│   ├── extract_data.py               # Data extraction and loading script
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Standalone extraction image
│   └── .dockerignore
└── food_delivery/                    # dbt project
    ├── dbt_project.yml
    ├── profiles.yml                  # BigQuery connection (not committed)
    └── models/
        ├── staging/
        │   ├── sources.yml
        │   ├── stg_deliveries.sql
        │   ├── stg_couriers.sql
        │   └── stg_zones.sql
        └── marts/
            ├── schema.yml
            ├── dim_couriers.sql
            ├── dim_zones.sql
            ├── fct_deliveries.sql
            └── mart_courier_performance.sql
```

---

## Pipeline

### Task 1: Extract and Load

`scripts/extract_data.py` generates synthetic food delivery data and loads it directly to BigQuery using the Python client library. Configured via environment variables — no hardcoded credentials.

Loads three raw tables to the `raw_data` dataset:

| Table | Rows | Description |
|-------|------|-------------|
| raw_deliveries | 1,000 | Delivery transactions |
| raw_couriers | 100 | Courier profiles |
| raw_zones | 20 | Geographic zones |

### Task 2: dbt Transformations

Seven models across three layers, materialized as views (staging) and tables (dims, fact, mart).

**Staging Layer** — clean and standardize raw data:
- `stg_deliveries` — filters to completed deliveries, calculates delivery time in minutes
- `stg_couriers` — filters to active couriers, calculates tenure in days
- `stg_zones` — combines city and zone name for display

**Marts Layer** — business-ready tables:
- `dim_couriers` — active courier lookup table with vehicle type and tenure
- `dim_zones` — geographic zones with city and region
- `fct_deliveries` — completed delivery transactions joined with courier and zone context
- `mart_courier_performance` — aggregated metrics per courier (delivery count, average time, total tips, average distance)

### Data Quality

26 passing tests covering:
- Primary key uniqueness on all dimension and fact tables
- Not null constraints on critical fields
- Referential integrity between fact and dimension tables
- Accepted values validation on categorical fields
- Positive value constraints on numeric metrics

---

## Docker Setup

The Airflow stack runs in Docker Compose with four services:

| Service | Purpose |
|---------|---------|
| postgres | Airflow metadata database |
| airflow-init | One-time database setup and user creation |
| airflow-webserver | UI at localhost:8080 |
| airflow-scheduler | DAG scheduling and task execution |

A custom Dockerfile extends the official Airflow image with dbt-bigquery installed at build time — not at runtime via `_PIP_ADDITIONAL_REQUIREMENTS`.

---

## Running the Project

### Prerequisites

- Docker Desktop
- Google Cloud Platform service account with BigQuery access
- Python 3.12 (for local dbt development)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/tnickster/food-delivery-analytics.git
cd food_delivery_analytics
```

2. Create a `.env` file in the project root:
```
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=.
PROJECT_ID=your-gcp-project-id
DATASET=raw_data
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/config/bigquery-key.json
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
```

3. Place your GCP service account key at `~/.dbt/bigquery-key.json`

4. Copy your dbt profiles file into the dbt project:
```bash
cp ~/.dbt/profiles.yml food_delivery/profiles.yml
```

5. Build and start the stack:
```bash
docker-compose build
docker-compose up -d
```

6. Open the Airflow UI at `http://localhost:8080` and trigger the `food_delivery_pipeline` DAG.

---

## DAG

The `food_delivery_pipeline` DAG runs on a daily schedule with two tasks:

```
extract_data  →  dbt_run
```

- `extract_data` — runs the Python extraction script to load fresh data to BigQuery
- `dbt_run` — runs all dbt models to transform raw data into analytics tables

---

## Author

Nicholas Tarazi — Courier Pay Analyst at Skip | Aspiring Data Engineer

[LinkedIn](https://www.linkedin.com/in/nicholas-tarazi/) | [GitHub](https://github.com/tnickster)
