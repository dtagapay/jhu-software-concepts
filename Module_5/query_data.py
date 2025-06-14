"""Command-line interface to run raw SQL queries on applicant data."""

import psycopg
from psycopg import sql

def create_connection():
    """Establish and return a PostgreSQL connection."""
    return psycopg.connect(
        host="127.0.0.1",
        port="5432",
        dbname="gradcafe_data",
        user="gradcafe",
        password="abc123"
    )

def run_query(cursor, label, base_query, params=None):
    """Execute a query and print labeled result."""
    try:
        cursor.execute(sql.SQL(base_query), params or [])
        result = cursor.fetchone()
        print(f"{label}: {result[0]}")
    except psycopg.Error as e:
        print(f"❌ Query failed ({label}):", e)

def run_all_queries():
    """Run all predefined applicant data queries."""
    with create_connection() as conn:
        with conn.cursor() as cursor:
            print("\n--- GradCafe Fall 2025 Insights ---\n")

            run_query(cursor, "1. Number of Fall 2025 entries",
                "SELECT COUNT(*) FROM applicants WHERE term ILIKE %s;",
                ['Fall 2025']
            )

            run_query(cursor, "2. % International Students",
                "SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM applicants), 2) "
                "FROM applicants WHERE us_or_international ILIKE %s;",
                ['International']
            )

            print("3. Averages (GPA, GRE, GRE V, GRE AW):")
            cursor.execute(sql.SQL(
                "SELECT ROUND(AVG(gpa)::numeric, 2), "
                "ROUND(AVG(gre)::numeric, 2), "
                "ROUND(AVG(gre_v)::numeric, 2), "
                "ROUND(AVG(gre_aw)::numeric, 2) "
                "FROM applicants;"
            ))
            result = cursor.fetchone()
            print(f"   GPA: {result[0]}, GRE: {result[1]}, GRE V: {result[2]}, GRE AW: {result[3]}")

            run_query(cursor, "4. Avg GPA (American, Fall 2025)",
                "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
                "WHERE us_or_international ILIKE %s AND term ILIKE %s;",
                ['American', 'Fall 2025']
            )

            run_query(cursor, "5. % Acceptances (Fall 2025)",
                "SELECT ROUND(100.0 * COUNT(*)::numeric / "
                "(SELECT COUNT(*) FROM applicants WHERE term ILIKE %s), 2) "
                "FROM applicants WHERE status ILIKE %s AND term ILIKE %s;",
                ['Fall 2025', '%Accepted%', 'Fall 2025']
            )

            run_query(cursor, "6. Avg GPA (Accepted, Fall 2025)",
                "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
                "WHERE status ILIKE %s AND term ILIKE %s;",
                ['%Accepted%', 'Fall 2025']
            )

            run_query(cursor, "7. Entries for JHU CS Master’s",
                "SELECT COUNT(*) FROM applicants "
                "WHERE program ILIKE %s AND program ILIKE %s AND degree ILIKE %s;",
                ['%Johns Hopkins%', '%Computer%', '%Master%']
            )

if __name__ == "__main__":
    run_all_queries()
