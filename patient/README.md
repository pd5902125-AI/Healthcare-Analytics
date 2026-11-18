# Hospital Patient and Healthcare Analytics Data Warehouse

Python, PostgreSQL, pandas, and a star-schema warehouse for hospital visit analysis.

## Project structure

- `data/hospital_visits.csv` — source sample data
- `sql/01_create_star_schema.sql` — PostgreSQL warehouse tables
- `sql/02_analysis_queries.sql` — reporting queries
- `src/etl_pipeline.py` — extraction, cleaning, validation, and loading
- `src/database_operations.py` — CREATE, UPDATE, DELETE, and SELECT demonstrations
- `docs/PROJECT_REPORT_TEMPLATE.md` — report template for the project discussion

## Setup

1. Install PostgreSQL and pgAdmin 4.
2. Create a database named `hospital_dw`.
3. Copy `.env.example` to `.env` and enter your credentials.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Create the star schema:

   Open `sql/01_create_star_schema.sql` in pgAdmin and execute it.

6. Run the ETL:

   `python src/etl_pipeline.py`

7. Run the database operations demonstration:

   `python src/database_operations.py`

## Security

Never commit `.env`. Use environment variables and a user account with only the privileges required for this project.

## Fact granularity

One row in `fact_hospital_activity` represents one patient hospital visit.
