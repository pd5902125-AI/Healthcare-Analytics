-- Admission rate
SELECT
    admission_status,
    COUNT(*) AS visits,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM fact_hospital_activity
GROUP BY admission_status
ORDER BY visits DESC;

-- Frequently reported medical conditions
SELECT c.diagnosis, COUNT(*) AS visit_count
FROM fact_hospital_activity f
JOIN dim_medical_condition c ON c.condition_key = f.condition_key
GROUP BY c.diagnosis
ORDER BY visit_count DESC, c.diagnosis;

-- Department workload and treatment expense
SELECT d.department_name,
       COUNT(*) AS visit_count,
       SUM(f.treatment_expense) AS total_expense,
       ROUND(AVG(f.treatment_expense), 2) AS average_expense
FROM fact_hospital_activity f
JOIN dim_department d ON d.department_key = f.department_key
GROUP BY d.department_name
ORDER BY visit_count DESC;

-- Visits over time
SELECT cal.year_number, cal.month_number, cal.month_name,
       COUNT(*) AS visit_count,
       SUM(f.treatment_expense) AS total_expense
FROM fact_hospital_activity f
JOIN dim_calendar cal ON cal.date_key = f.date_key
GROUP BY cal.year_number, cal.month_number, cal.month_name
ORDER BY cal.year_number, cal.month_number;

-- Physician activity
SELECT p.physician_name, COUNT(*) AS visit_count,
       SUM(f.treatment_expense) AS treatment_expenses
FROM fact_hospital_activity f
JOIN dim_physician p ON p.physician_key = f.physician_key
GROUP BY p.physician_name
ORDER BY visit_count DESC;
