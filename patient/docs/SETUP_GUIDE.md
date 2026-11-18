# PostgreSQL Setup Guide

## 1. Install dependencies

In PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Create the database

In pgAdmin 4:

1. Connect to your PostgreSQL server.
2. Right-click **Databases** and select **Create > Database**.
3. Name it `hospital_dw`.

## 3. Configure credentials

```powershell
Copy-Item .env.example .env
```

Edit `.env` and enter the actual password and port. Do not share or commit this file.

## 4. Create tables

Open `sql/01_create_star_schema.sql` in pgAdmin, select the `hospital_dw` database, and execute the script.

## 5. Load data

```powershell
python src/etl_pipeline.py
```

## 6. Run database operations

```powershell
python src/database_operations.py
```

## 7. Run analysis

Open `sql/02_analysis_queries.sql` in pgAdmin and execute individual statements.

## Troubleshooting

- `password authentication failed`: verify `.env` credentials.
- `connection refused`: verify PostgreSQL service and port.
- `relation does not exist`: execute the star schema script first.
- `psycopg2` import error: activate the virtual environment and reinstall requirements.
