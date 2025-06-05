from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def create_connection():
    return psycopg2.connect(
        dbname="gradcafe_data",
        user="gradcafe",
        password="abc123",  # update if needed
        host="127.0.0.1",
        port="5432"
    )

def run_queries():
    conn = create_connection()
    cursor = conn.cursor()

    def q(sql):
        cursor.execute(sql)
        return cursor.fetchone()[0]

    # Queries (same logic as query_data.py but returned as a dictionary)
    results = {
        "fall_2025_count": q("SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025';"),
        "international_pct": q(
            "SELECT ROUND(100.0 * COUNT(*)::numeric / (SELECT COUNT(*) FROM applicants), 2) "
            "FROM applicants WHERE us_or_international ILIKE 'International';"
        ),
        "gpa_avg": None,
        "gre_avg": None,
        "gre_v_avg": None,
        "gre_aw_avg": None,
        "american_gpa_fall_2025": q(
            "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
            "WHERE us_or_international ILIKE 'American' AND term ILIKE 'Fall 2025';"
        ),
        "fall_2025_accept_pct": q(
            "SELECT ROUND(100.0 * COUNT(*)::numeric / "
            "(SELECT COUNT(*) FROM applicants WHERE term ILIKE 'Fall 2025'), 2) "
            "FROM applicants WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';"
        ),
        "fall_2025_accept_gpa_avg": q(
            "SELECT ROUND(AVG(gpa)::numeric, 2) FROM applicants "
            "WHERE status ILIKE '%Accepted%' AND term ILIKE 'Fall 2025';"
        ),
        "jhu_cs_masters_count": q(
            "SELECT COUNT(*) FROM applicants "
            "WHERE program ILIKE '%Johns Hopkins%' AND program ILIKE '%Computer%' AND degree ILIKE '%Master%';"
        ),
    }

    # Separate GPA/GRE AVG block
    cursor.execute("""
        SELECT 
            ROUND(AVG(gpa)::numeric, 2), 
            ROUND(AVG(gre)::numeric, 2), 
            ROUND(AVG(gre_v)::numeric, 2), 
            ROUND(AVG(gre_aw)::numeric, 2)
        FROM applicants;
    """)
    gpa_block = cursor.fetchone()
    results["gpa_avg"], results["gre_avg"], results["gre_v_avg"], results["gre_aw_avg"] = gpa_block

    conn.close()
    return results

@app.route("/")
def index():
    results = run_queries()
    return render_template("index.html", **results)

if __name__ == "__main__":
    app.run(debug=True)
