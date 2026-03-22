# Food Delivery Analytics Pipeline

An end-to-end analytics pipeline for food delivery operations, built with dbt and BigQuery. This project transforms raw delivery data into business-ready analytics tables and pre-calculated metrics for dashboards.

## Project Overview

This project demonstrates production-grade data engineering practices including dimensional modeling, data quality testing, and comprehensive documentation. The pipeline processes delivery transactions, courier information, and geographic zones to provide actionable insights on courier performance and operational metrics.

**Built to showcase:**
- Data modeling (staging → dimensions → facts → marts)
- SQL transformations with dbt
- Data quality testing (17 tests)
- Complete documentation
- Version control with Git

## Tech Stack

- **Transformation:** dbt (Data Build Tool) 1.7
- **Data Warehouse:** Google BigQuery
- **Languages:** SQL, Python
- **Version Control:** Git

## Data Pipeline Architecture
```
Raw Sources (BigQuery)
  └─ raw_deliveries (1,000 rows)
  └─ raw_couriers (100 rows)  
  └─ raw_zones (20 zones)
       ↓
Staging Layer (Clean & Standardize)
  └─ stg_deliveries (filters completed, calculates delivery time)
  └─ stg_couriers (filters active, calculates tenure)
  └─ stg_zones (creates full location names)
       ↓
Marts Layer (Business Logic)
  └─ dim_couriers (courier lookup table - 77 active couriers)
  └─ dim_zones (geographic zones - 20 zones)
  └─ fct_deliveries (delivery transactions with full context - 624 deliveries)
  └─ mart_courier_performance (aggregated courier metrics)
```

## Project Structure
```
food_delivery_analytics/
├── food_delivery/               # dbt project
│   ├── models/
│   │   ├── staging/
│   │   │   ├── sources.yml      # Source definitions
│   │   │   ├── stg_deliveries.sql
│   │   │   ├── stg_couriers.sql
│   │   │   └── stg_zones.sql
│   │   └── marts/
│   │       ├── dim_couriers.sql
│   │       ├── dim_zones.sql
│   │       ├── fct_deliveries.sql
│   │       ├── mart_courier_performance.sql
│   │       └── schema.yml       # Tests & documentation
│   └── dbt_project.yml
├── scripts/
│   └── generate_data.py         # Mock data generator
└── README.md
```

## Models

### Staging Layer
- **stg_deliveries:** Filters to completed deliveries, calculates delivery time in minutes
- **stg_couriers:** Filters to active couriers, calculates days since signup
- **stg_zones:** Combines city and zone name for display

### Marts Layer
- **dim_couriers:** Lookup table containing active courier information (vehicle type, signup date, tenure)
- **dim_zones:** Geographic zones with city and region information
- **fct_deliveries:** Fact table joining deliveries with courier and zone context (624 completed deliveries with assigned couriers)
- **mart_courier_performance:** Aggregated metrics per courier (total deliveries, average delivery time, total tips, average distance)

## Data Quality

- **17 passing tests** including:
  - Primary key uniqueness (delivery_id, courier_id, zone_id)
  - Not null constraints on critical fields
  - Data integrity across the pipeline

## Setup & Installation

### Prerequisites
- Python 3.12+
- Google Cloud Platform account
- BigQuery project

### Installation Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd food_delivery_analytics
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install dbt-bigquery
```

4. **Configure BigQuery connection**
- Place your service account JSON key in `~/.dbt/`
- Update `~/.dbt/profiles.yml` with your project details

5. **Generate mock data**
```bash
python scripts/generate_data.py
```

6. **Upload CSVs to BigQuery**
- Create `raw_data` dataset in BigQuery
- Upload `raw_deliveries.csv`, `raw_couriers.csv`, `raw_zones.csv`

7. **Run dbt**
```bash
cd food_delivery
dbt deps
dbt run
dbt test
```

8. **View documentation**
```bash
dbt docs generate
dbt docs serve
```

## Key Insights

This pipeline enables analysis of:
- **Courier Performance:** Average delivery times, total tips earned, delivery volume by courier
- **Geographic Trends:** Delivery volumes and performance by zone
- **Operational Metrics:** Delivery time distribution, tip patterns, distance analysis
- **Vehicle Efficiency:** Performance comparison across vehicle types (bike, car, scooter, ebike)

## Skills Demonstrated

- **Data Modeling:** Dimensional modeling with staging, facts, and dimensions
- **SQL:** Complex joins, window functions, aggregations
- **dbt:** Models, tests, documentation, Jinja templating
- **Data Quality:** Comprehensive testing strategy
- **Version Control:** Git workflow
- **Documentation:** Schema documentation and project README

## Future Enhancements

- Implement incremental models for large-scale data
- Add Python extraction layer for automated data ingestion
- Create Airflow DAG for pipeline orchestration
- Add snapshot models for slowly changing dimensions
- Implement advanced custom tests

## Author

**Nicholas Tarazi** - Courier Pay Analyst at Skip | Aspiring Data Engineer  
[LinkedIn](https://www.linkedin.com/in/nicholas-tarazi/)

---

*This project was built as a portfolio piece to demonstrate data engineering capabilities with modern tools and best practices.*