"""Module to create table and load applicant JSON data into PostgreSQL."""

import json
import psycopg
from psycopg import sql

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Connect to PostgreSQL database and return the connection."""
    return psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )

def create_table(db_conn):
    """Create the applicants table if it doesn't exist."""
    with db_conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applicants (
                p_id SERIAL PRIMARY KEY,
                program TEXT,
                comments TEXT,
                date_added DATE,
                url TEXT,
                status TEXT,
                term TEXT,
                us_or_international TEXT,
                gpa FLOAT,
                gre FLOAT,
                gre_v FLOAT,
                gre_aw FLOAT,
                degree TEXT
            );
        """)
        db_conn.commit()
        print("✅ Table 'applicants' ensured")

def clean_score(value):
    """Convert a score to float, return None if invalid or 0.0."""
    try:
        val = float(value)
        if val == 0.0:
            return None
        return val
    except (ValueError, TypeError):
        return None

def load_data(db_conn, filepath="applicant_data.json"):
    """Load JSON file into the applicants table."""
    with db_conn.cursor() as cursor:
        # Clear existing data
        cursor.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier("applicants")))
        db_conn.commit()
        print("🧹 Existing data cleared from 'applicants'")

        # Load and parse JSON
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        insert_query = sql.SQL("""
            INSERT INTO {table} (
                program, comments, date_added, url, status, term,
                us_or_international, gpa, gre, gre_v, gre_aw, degree
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """).format(table=sql.Identifier("applicants"))

        for row in data:
            try:
                values = (
                    row.get("program"),
                    row.get("comments"),
                    row.get("date_added"),
                    row.get("url"),
                    row.get("status"),
                    row.get("term"),
                    row.get("US/International"),
                    clean_score(row.get("GPA")),
                    clean_score(row.get("GRE")),
                    clean_score(row.get("GRE V")),
                    clean_score(row.get("GRE AW")),
                    row.get("Degree")
                )
                cursor.execute(insert_query, values)
            except Exception as e:
                print(f"⚠️ Skipped entry due to error: {e}\nData: {row}")

        db_conn.commit()
        print("✅ All valid entries loaded into database")

if __name__ == "__main__":
    with create_connection(
        "gradcafe_data", "gradcafe", "abc123", "127.0.0.1", "5432"
    ) as conn:
        create_table(conn)
        load_data(conn)
