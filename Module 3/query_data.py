import psycopg2

# --- DB Connection ---
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="gradcafe_data",
            user="gradcafe",
            password="abc123",  # replace with your actual password
            host="127.0.0.1",
            port="5432"
        )
        print("✅ Connected to database")
        return conn
    except Exception as e:
        print("❌ Connection failed:", e)
        return None

# --- Query Helper ---
def run_query(conn, label, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        print(f"{label}: {result[0]}")
    except Exception as e:
        print(f"❌ Query failed ({label}):", e)

# --- Main Queries ---
def run_all_queries(conn):
    print("\n--- GradCafe Fall 2025 Insights ---\n")

    # 1. Count of entries for Fall 2025
    run_query(conn, "1. Number of Fall 2025 entries",
        "SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025';")

    # 2. % of international students
    run_query(conn, "2. % International Students",
        "SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM applicants), 2) "
        "FROM applicants WHERE us_or_international ILIKE 'International';")

    # 3. Average GPA, GRE, GRE V, GRE AW
    cursor = conn.cursor()
    print("3. Averages (GPA, GRE, GRE V, GRE AW):")
    cursor.execute("""
        SELECT 
            ROUND(AVG(gpa)::numeric, 2), 
            ROUND(AVG(gre)::numeric, 2), 
            ROUND(AVG(gre_v)::numeric, 2), 
            ROUND(AVG(gre_aw)::numeric, 2)
        FROM applicants;
    """)

    result = cursor.fetchone()
    print(f"   GPA: {result[0]}, GRE: {result[1]}, GRE V: {result[2]}, GRE AW: {result[3]}")

    # 4. Average GPA of American students for Fall 2025
    run_query(conn, "4. Avg GPA (American, Fall 2025)",
        "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
        "WHERE us_or_international ILIKE 'American' AND term ILIKE 'Fall 2025';")

    # 5. % of acceptances for Fall 2025
    run_query(conn, "5. % Acceptances (Fall 2025)",
        "SELECT ROUND(100.0 * COUNT(*) / "
        "(SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025'), 2) "
        "FROM applicants WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';")

    # 6. Avg GPA of accepted Fall 2025 applicants
    run_query(conn, "6. Avg GPA (Accepted, Fall 2025)",
        "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
        "WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';")

    # 7. Entries for JHU, CS, Master's (all entries, not just Fall 2025)
    run_query(conn, "7. Entries for JHU CS Master’s",
        "SELECT COUNT(*) FROM applicants "
        "WHERE program ILIKE '%Johns Hopkins%' AND program ILIKE '%Computer%' AND degree ILIKE '%Master%';")

# --- Main ---
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        run_all_queries(conn)
        conn.close()
