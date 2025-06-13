"""Command-line interface to run raw SQL queries on applicant data."""

import psycopg2

def create_connection():
    """Establish and return a PostgreSQL connection."""
    return psycopg2.connect(
        host="127.0.0.1",
        port="5432",
        dbname="gradcafe_data",
        user="gradcafe",
        password="abc123"
    )

# --- Query Helper ---
def run_query(db_conn, label, query):
    """Execute a query and print labeled result."""
    cursor = db_conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"{label}: {result[0]}")
    except psycopg2.Error as e:
        print(f"❌ Query failed ({label}):", e)
        db_conn.rollback()

# --- Main Queries ---
def run_all_queries(db_conn):
    """Run all predefined applicant data queries."""
    print("\n--- GradCafe Fall 2025 Insights ---\n")

    run_query(db_conn, "1. Number of Fall 2025 entries",
        "SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025';")

    run_query(db_conn, "2. % International Students",
        "SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM applicants), 2) "
        "FROM applicants WHERE us_or_international ILIKE 'International';")

    print("3. Averages (GPA, GRE, GRE V, GRE AW):")
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT ROUND(AVG(gpa)::numeric, 2), "
        "ROUND(AVG(gre)::numeric, 2), "
        "ROUND(AVG(gre_v)::numeric, 2), "
        "ROUND(AVG(gre_aw)::numeric, 2) "
        "FROM applicants;"
    )
    result = cursor.fetchone()
    print(f"   GPA: {result[0]}, GRE: {result[1]}, GRE V: {result[2]}, GRE AW: {result[3]}")

    run_query(db_conn, "4. Avg GPA (American, Fall 2025)",
        "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
        "WHERE us_or_international ILIKE 'American' AND term ILIKE 'Fall 2025';")

    run_query(db_conn, "5. % Acceptances (Fall 2025)",
        "SELECT ROUND(100.0 * COUNT(*)::numeric / "
        "(SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025'), 2) "
        "FROM applicants WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';")

    run_query(db_conn, "6. Avg GPA (Accepted, Fall 2025)",
        "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
        "WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';")

    run_query(db_conn, "7. Entries for JHU CS Master’s",
        "SELECT COUNT(*) FROM applicants "
        "WHERE program ILIKE '%Johns Hopkins%' "
        "AND program ILIKE '%Computer%' AND degree ILIKE '%Master%';")

# --- Main ---
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        run_all_queries(conn)
        conn.close()
