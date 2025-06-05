import json
import psycopg2
from psycopg2 import OperationalError

# -------- HELPER: Safely convert strings to float or return None --------
def safe_float(val):
    try:
        f = float(val)
        if f == 0.0:
            return None  # treat "0" or 0.0 as missing data
        return f
    except:
        return None

# -------- DATABASE CONNECTION SETUP --------
DB_NAME   = "gradcafe_data"
DB_USER   = "gradcafe"
DB_PASS   = "abc123"      # <-- update if needed
DB_HOST   = "127.0.0.1"
DB_PORT   = "5432"

def create_connection():
    """
    Establish and return a connection to PostgreSQL using psycopg2.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )
        print(f"✅ Connection to PostgreSQL DB '{DB_NAME}' successful")
    except OperationalError as e:
        print(f"❌ The error '{e}' occurred")
    return connection

# -------- CREATE TABLE IF NOT EXISTS --------
def create_table(conn):
    """
    Create the 'applicants' table if it doesn't exist already.
    """
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
        gpa FLOAT,       -- FLOAT columns allow NULL by default
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

# -------- LOAD JSON AND INSERT INTO TABLE --------
def load_data(conn, filepath="applicant_data.json"):
    """
    Read applicant_data.json, convert fields safely, and insert rows into 'applicants'.
    Missing or non‐numeric GPAs/GREs become NULL instead of 0.0.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    cursor = conn.cursor()
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
                safe_float(row.get("GPA")),       # None if missing/invalid
                safe_float(row.get("GRE")),       # None if missing/invalid
                safe_float(row.get("GRE V")),     # None if missing/invalid
                safe_float(row.get("GRE AW")),    # None if missing/invalid
                row.get("Degree")
            ))
        except Exception as e:
            print(f"⚠️ Skipped entry due to error: {e}\nData: {row}")

    conn.commit()
    print("✅ All valid entries loaded into database")

# -------- MAIN EXECUTION --------
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_table(conn)
        load_data(conn)
        conn.close()
