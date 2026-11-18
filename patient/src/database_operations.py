import psycopg2
from psycopg2.extras import RealDictCursor

from db_config import get_connection


def print_rows(title, rows):
    print(f"\n{title}")
    if not rows:
        print("No records found.")
        return
    for row in rows:
        print(dict(row))


def run_operations():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # CREATE: create a project-specific log table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_operation_log (
                operation_id SERIAL PRIMARY KEY,
                operation_name VARCHAR(50) NOT NULL,
                table_name VARCHAR(50) NOT NULL,
                details TEXT,
                operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # CREATE: insert a temporary physician demonstration record.
        cursor.execute("""
            INSERT INTO dim_physician (physician_name)
            VALUES ('Dr. Test Physician')
            ON CONFLICT (physician_name) DO UPDATE
            SET physician_name = EXCLUDED.physician_name
            RETURNING physician_key, physician_name
        """)
        created = cursor.fetchone()
        print_rows("Created physician record:", [created])

        # UPDATE: update the demonstration physician name.
        cursor.execute("""
            UPDATE dim_physician
            SET physician_name = 'Dr. Updated Physician'
            WHERE physician_name = 'Dr. Test Physician'
            RETURNING physician_key, physician_name
        """)
        updated = cursor.fetchone()
        print_rows("Updated physician record:", [updated] if updated else [])

        # SELECT: retrieve records as dictionaries using RealDictCursor.
        cursor.execute("""
            SELECT physician_key, physician_name
            FROM dim_physician
            WHERE physician_name LIKE 'Dr. %%'
            ORDER BY physician_name
            LIMIT 10
        """)
        print_rows("Physicians retrieved as dictionaries:", cursor.fetchall())

        # DELETE: remove only the demonstration record.
        cursor.execute("""
            DELETE FROM dim_physician
            WHERE physician_name = 'Dr. Updated Physician'
            RETURNING physician_key, physician_name
        """)
        deleted = cursor.fetchall()
        print_rows("Deleted physician record:", deleted)

        cursor.execute("""
            INSERT INTO project_operation_log (operation_name, table_name, details)
            VALUES
                ('CREATE', 'dim_physician', 'Inserted Dr. Test Physician'),
                ('UPDATE', 'dim_physician', 'Renamed physician to Dr. Updated Physician'),
                ('DELETE', 'dim_physician', 'Removed demonstration physician')
        """)

        cursor.execute("""
            SELECT operation_id, operation_name, table_name, details, operation_time
            FROM project_operation_log
            ORDER BY operation_id DESC
            LIMIT 10
        """)
        print_rows("Operation log:", cursor.fetchall())

        conn.commit()
        print("\nAll database operations committed successfully.")

    except psycopg2.Error as error:
        conn.rollback()
        print(f"Database error: {error}")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    run_operations()
