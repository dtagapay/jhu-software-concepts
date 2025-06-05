import json
import psycopg2
from psycopg2 import OperationalError

# Function to connect to PostgreSQL
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print(f"✅ Connection to PostgreSQL DB '{db_name}' successful")
    except OperationalError as e:
        print(f"❌ The error '{e}' occurred")
    return connection

# Function to create the applicants table
def create_table(conn):
    query = """
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
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("✅ Table 'applicants' ensured")

# Clean GPA/GRE-style fields
def clean_score(value):
    try:
        val = float(value)
        if val == 0.0:
            return None
        return val
    except (ValueError, TypeError):
        return None

# Load JSON into the applicants table
def load_data(conn, filepath="applicant_data.json"):
    cursor = conn.cursor()

    # 🧹 Clear existing data
    cursor.execute("DELETE FROM applicants;")
    conn.commit()
    print("🧹 Existing data cleared from 'applicants'")

    # Load and parse JSON
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    for row in data:
        try:
            cursor.execute("""
                INSERT INTO applicants (
                    program, comments, date_added, url, status, term,
                    us_or_international, gpa, gre, gre_v, gre_aw, degree
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
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
            ))
        except Exception as e:
            print(f"⚠️ Skipped entry due to error: {e}\nData: {row}")
    
    conn.commit()
    print("✅ All valid entries loaded into database")

# MAIN
if __name__ == "__main__":
    conn = create_connection(
        "gradcafe_data", "gradcafe", "abc123", "127.0.0.1", "5432"
    )
    if conn:
        create_table(conn)
        load_data(conn)
        conn.close()
