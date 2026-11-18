from pathlib import Path

import pandas as pd
import psycopg2.extras

from db_config import get_connection

SOURCE_FILE = Path(__file__).resolve().parent.parent / "data" / "hospital_visits.csv"


def extract():
    return pd.read_csv(SOURCE_FILE, dtype={"patient_number": str})


def transform(df):
    original_rows = len(df)

    df = df.copy()
    df.columns = [column.strip().lower() for column in df.columns]
    df = df.drop_duplicates()

    df["patient_number"] = df["patient_number"].astype("string").str.strip().str.upper()
    df["gender"] = df["gender"].astype("string").str.strip().str.title()
    df["attending_physician"] = df["attending_physician"].astype("string").str.strip()
    df["medical_department"] = df["medical_department"].astype("string").str.strip().str.title()
    df["diagnosis"] = df["diagnosis"].astype("string").str.strip().str.title()
    df["admission_status"] = df["admission_status"].astype("string").str.strip().str.title()

    df["patient_age"] = pd.to_numeric(df["patient_age"], errors="coerce")
    df.loc[(df["patient_age"] < 0) | (df["patient_age"] > 120), "patient_age"] = pd.NA
    df["treatment_expense"] = pd.to_numeric(df["treatment_expense"], errors="coerce")
    df.loc[df["treatment_expense"] < 0, "treatment_expense"] = pd.NA

    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce")

    valid = df[
        df["patient_number"].notna()
        & df["attending_physician"].notna()
        & df["medical_department"].notna()
        & df["diagnosis"].notna()
        & df["visit_date"].notna()
        & df["treatment_expense"].notna()
    ].copy()

    duplicate_count = int(df.duplicated(subset=[
        "patient_number", "attending_physician", "medical_department",
        "diagnosis", "visit_date", "admission_status"
    ]).sum())
    valid = valid.drop_duplicates(subset=[
        "patient_number", "attending_physician", "medical_department",
        "diagnosis", "visit_date", "admission_status"
    ])

    report = {
        "source_rows": original_rows,
        "rows_after_duplicate_removal": len(valid),
        "invalid_or_incomplete_rows_removed": len(df) - len(valid) - duplicate_count,
        "duplicate_visits_removed": duplicate_count,
    }
    return valid, report


def get_or_create_dimension(cur, table, key_column, value_column, value):
    cur.execute(
        f"INSERT INTO {table} ({value_column}) VALUES (%s) "
        f"ON CONFLICT ({value_column}) DO UPDATE SET {value_column} = EXCLUDED.{value_column} "
        f"RETURNING {key_column}",
        (value,),
    )
    return cur.fetchone()[key_column]


def load(df):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    loaded = 0

    try:
        for row in df.itertuples(index=False):
            patient_key = get_or_create_dimension(cur, "dim_patient", "patient_key", "patient_number", row.patient_number)

            cur.execute(
                "UPDATE dim_patient SET patient_age = %s, gender = %s WHERE patient_key = %s",
                (None if pd.isna(row.patient_age) else int(row.patient_age),
                 None if pd.isna(row.gender) else row.gender,
                 patient_key),
            )

            physician_key = get_or_create_dimension(cur, "dim_physician", "physician_key", "physician_name", row.attending_physician)
            department_key = get_or_create_dimension(cur, "dim_department", "department_key", "department_name", row.medical_department)
            condition_key = get_or_create_dimension(cur, "dim_medical_condition", "condition_key", "diagnosis", row.diagnosis)

            visit_date = row.visit_date.date()
            date_key = int(visit_date.strftime("%Y%m%d"))
            cur.execute("""
                INSERT INTO dim_calendar
                (date_key, full_date, day_of_month, month_number, month_name, quarter_number, year_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (date_key) DO NOTHING
            """, (
                date_key, visit_date, visit_date.day, visit_date.month,
                visit_date.strftime("%B"), (visit_date.month - 1) // 3 + 1,
                visit_date.year,
            ))

            cur.execute("""
                INSERT INTO fact_hospital_activity
                (patient_key, physician_key, department_key, condition_key, date_key,
                 admission_status, treatment_expense, visit_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                ON CONFLICT (patient_key, physician_key, department_key, condition_key, date_key)
                DO UPDATE SET
                    admission_status = EXCLUDED.admission_status,
                    treatment_expense = EXCLUDED.treatment_expense
                RETURNING visit_key
            """, (
                patient_key, physician_key, department_key, condition_key, date_key,
                row.admission_status, float(row.treatment_expense),
            ))
            loaded += 1

        conn.commit()
        print(f"ETL completed. Processed {loaded} valid visit records.")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def main():
    print("Starting ETL pipeline...")
    source = extract()
    cleaned, report = transform(source)
    print("Data quality report:", report)
    load(cleaned)


if __name__ == "__main__":
    main()
