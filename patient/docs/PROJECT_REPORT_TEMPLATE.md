# Hospital Patient and Healthcare Analytics Data Warehouse

## Project Discussion #2 — Python–PostgreSQL Database Connectivity

**Student:** ____________________  
**Course:** ____________________  
**Date:** November 18, 2026  

## 1. Project Overview

This project implements a PostgreSQL hospital data warehouse using Python, pandas, `psycopg2`, and `psycopg2.extras.RealDictCursor`. The star schema contains one fact table, `fact_hospital_activity`, and five dimensions: `dim_patient`, `dim_physician`, `dim_department`, `dim_medical_condition`, and `dim_calendar`. Each fact row represents one patient visit.

## 2. Database Environment

- PostgreSQL database: `hospital_dw`
- Database tool: pgAdmin 4
- Python package: `psycopg2-binary`
- Cursor type: `psycopg2.extras.RealDictCursor`
- Source data: `data/hospital_visits.csv`

## 3. Setup and Execution

Paste the screenshots or link the GitHub repository below.

### 3.1 Database Connection

Screenshot: successful PostgreSQL connection.

```text
Paste screenshot here or add evidence link.
```

### 3.2 Star Schema Creation

Screenshot: execution of `sql/01_create_star_schema.sql`.

```text
Paste screenshot here or add evidence link.
```

### 3.3 ETL Execution

Screenshot: Python ETL code and successful output.

```text
Paste screenshot here or add evidence link.
```

## 4. CREATE Operation

The Python script created the `project_operation_log` table and inserted a demonstration physician record using parameterized SQL.

**Code evidence:** `src/database_operations.py`

**Before screenshot:** pgAdmin table browser before operation.

**After screenshot:** inserted `Dr. Test Physician` record.

## 5. UPDATE Operation

The script updated `Dr. Test Physician` to `Dr. Updated Physician`.

**Code evidence:** parameterized `UPDATE` statement in `src/database_operations.py`

**After screenshot:** updated row in pgAdmin.

## 6. SELECT Operation

The script used `psycopg2.extras.RealDictCursor` and converted returned rows to dictionaries.

**Code evidence:** `SELECT` physician query and `print(dict(row))` output.

**Execution screenshot:** Python console output.

## 7. DELETE Operation

The script deleted only the demonstration physician named `Dr. Updated Physician`.

**Code evidence:** parameterized `DELETE` statement.

**After screenshot:** row removed from pgAdmin.

## 8. Data Quality and ETL Results

Document the ETL report output here:

- Source rows:
- Duplicate visits removed:
- Invalid or incomplete rows removed:
- Valid rows loaded:

## 9. Other Relevant Operations

The script also:

- Uses transactions and `commit()`.
- Rolls back changes if a database exception occurs.
- Closes the cursor and connection.
- Writes CREATE, UPDATE, and DELETE actions to `project_operation_log`.

## 10. SQL Analysis Evidence

Run queries in `sql/02_analysis_queries.sql` and place the screenshots below:

1. Admission rates
2. Most frequent conditions
3. Department workload
4. Treatment expense trends
5. Visits over time

## 11. Conclusion

Describe what was successfully implemented, the data warehouse benefit, and PostgreSQL verification results.

## 12. References

- PostgreSQL documentation
- psycopg2 documentation
- pandas documentation
- Course-provided PostgreSQL and Python exercise
