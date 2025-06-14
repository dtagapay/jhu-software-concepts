"""Flask web app for displaying GradCafe data."""
from flask import Flask, render_template
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def create_connection():
    """Establish and return a PostgreSQL database connection."""
    return psycopg2.connect(
        dbname="gradcafe_data",
        user="gradcafe",
        password="abc123",
        host="127.0.0.1",
        port="5432"
    )

def run_queries():
    """Run SQL queries and return results as a dictionary."""
    conn = create_connection()
    cursor = conn.cursor()

    def q_safe(base_query, params=None):
        cursor.execute(sql.SQL(base_query), params or [])
        return cursor.fetchone()[0]

    results = {
        "fall_2025_count": q_safe(
            "SELECT COUNT(*) FROM applicants WHERE term ILIKE %s;",
            ['Fall 2025']
        ),
        "international_pct": q_safe(
            "SELECT ROUND(100.0 * COUNT(*)::numeric / "
            "(SELECT COUNT(*) FROM applicants), 2) "
            "FROM applicants WHERE us_or_international ILIKE %s;",
            ['International']
        ),
        "gpa_avg": None,
        "gre_avg": None,
        "gre_v_avg": None,
        "gre_aw_avg": None,
        "american_gpa_fall_2025": q_safe(
            "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
            "WHERE us_or_international ILIKE %s AND term ILIKE %s;",
            ['American', 'Fall 2025']
        ),
        "fall_2025_accept_pct": q_safe(
            "SELECT ROUND(100.0 * COUNT(*)::numeric / "
            "(SELECT COUNT(*) FROM applicants WHERE term ILIKE %s), 2) "
            "FROM applicants WHERE status ILIKE %s AND term ILIKE %s;",
            ['Fall 2025', '%Accepted%', 'Fall 2025']
        ),
        "fall_2025_accept_gpa_avg": q_safe(
            "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
            "WHERE status ILIKE %s AND term ILIKE %s;",
            ['%Accepted%', 'Fall 2025']
        ),
        "jhu_cs_masters_count": q_safe(
            "SELECT COUNT(*) FROM applicants WHERE "
            "program ILIKE %s AND program ILIKE %s AND degree ILIKE %s;",
            ['%Johns Hopkins%', '%Computer%', '%Master%']
        ),
    }

    # Secure GPA/GRE average query (no user input required)
    cursor.execute(sql.SQL("""
        SELECT 
            ROUND(AVG(gpa)::numeric, 2), 
            ROUND(AVG(gre)::numeric, 2), 
            ROUND(AVG(gre_v)::numeric, 2), 
            ROUND(AVG(gre_aw)::numeric, 2)
        FROM applicants;
    """))
    gpa_block = cursor.fetchone()
    (
        results["gpa_avg"],
        results["gre_avg"],
        results["gre_v_avg"],
        results["gre_aw_avg"]
    ) = gpa_block

    conn.close()
    return results

@app.route("/")
def index():
    """Render homepage with query results."""
    results = run_queries()
    return render_template("index.html", **results)

if __name__ == "__main__":
    app.run(debug=True)

