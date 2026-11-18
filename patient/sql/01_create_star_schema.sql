-- Hospital Patient and Healthcare Analytics Star Schema
-- Run in the hospital_dw PostgreSQL database.

CREATE TABLE IF NOT EXISTS dim_patient (
    patient_key SERIAL PRIMARY KEY,
    patient_number VARCHAR(20) NOT NULL UNIQUE,
    patient_age INTEGER CHECK (patient_age IS NULL OR patient_age BETWEEN 0 AND 120),
    gender VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_physician (
    physician_key SERIAL PRIMARY KEY,
    physician_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_department (
    department_key SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_medical_condition (
    condition_key SERIAL PRIMARY KEY,
    diagnosis VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_calendar (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_month INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INTEGER NOT NULL,
    year_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_hospital_activity (
    visit_key SERIAL PRIMARY KEY,
    patient_key INTEGER NOT NULL REFERENCES dim_patient(patient_key),
    physician_key INTEGER NOT NULL REFERENCES dim_physician(physician_key),
    department_key INTEGER NOT NULL REFERENCES dim_department(department_key),
    condition_key INTEGER NOT NULL REFERENCES dim_medical_condition(condition_key),
    date_key INTEGER NOT NULL REFERENCES dim_calendar(date_key),
    admission_status VARCHAR(30) NOT NULL,
    treatment_expense NUMERIC(12,2) NOT NULL CHECK (treatment_expense >= 0),
    visit_count INTEGER NOT NULL DEFAULT 1,
    UNIQUE (patient_key, physician_key, department_key, condition_key, date_key)
);

CREATE INDEX IF NOT EXISTS idx_fact_patient ON fact_hospital_activity(patient_key);
CREATE INDEX IF NOT EXISTS idx_fact_department ON fact_hospital_activity(department_key);
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_hospital_activity(date_key);
