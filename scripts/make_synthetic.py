"""
Generate a SYNTHETIC CSV with the same schema as lukebarousse/data_jobs.

Offline plan B for the seminar and a way to test the scripts without network.
The data is made up: it must never be used to draw real conclusions.

Usage:
    uv run scripts/make_synthetic.py                  # 786,000 rows
    uv run scripts/make_synthetic.py --rows 200000
"""

import argparse

import duckdb

from download_data import SYNTHETIC_CSV
from common import format_int

SKILLS = [
    "sql", "python", "r", "excel", "tableau", "power bi", "aws", "azure",
    "spark", "nosql", "mysql", "postgresql", "sql server", "java", "scala",
    "go", "c", "pandas", "airflow", "docker", "kubernetes", "git", "snowflake",
]
TITLES = [
    "Data Analyst", "Data Engineer", "Data Scientist", "Senior Data Engineer",
    "Senior Data Analyst", "Business Analyst", "Machine Learning Engineer",
    "Software Engineer", "Senior Data Scientist", "Cloud Engineer",
]
COUNTRIES = ["United States", "India", "United Kingdom", "Germany", "France",
             "Spain", "Canada", "Netherlands", "Brazil", "Mexico"]


def sql_list(values):
    return "[" + ", ".join(f"'{v}'" for v in values) + "]"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rows", type=int, default=786_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    SYNTHETIC_CSV.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect()
    # Deterministic randomness: every value comes from hash(row, slot, seed).
    # random() with several threads gives different data on each run even with a seed.
    connection.sql(f"CREATE MACRO rnd(i, k) AS (hash(i * 1000 + k + {args.seed} * 7919) % 1000000) / 1000000.0")
    skills, titles, countries = sql_list(SKILLS), sql_list(TITLES), sql_list(COUNTRIES)
    connection.sql(f"""
        CREATE TABLE base AS
        SELECT i,
               {titles}[1 + (rnd(i, 1) * {len(TITLES) - 1})::INT] AS job_title_short,
               {countries}[1 + (rnd(i, 2) * {len(COUNTRIES) - 1})::INT] AS job_country,
               rnd(i, 3) AS r_skills, rnd(i, 4) AS r_salary, rnd(i, 5) AS r_type,
               1 + (rnd(i, 6) * 7)::INT AS n_skills
        FROM range({args.rows}) t(i)
    """)
    # Same traps as the real data: skills stored as Python-style list text,
    # repeated skills inside a posting, and salary missing for about 97 % of rows.
    connection.sql(f"""
        CREATE TABLE postings AS
        SELECT job_title_short,
               job_title_short || CASE WHEN r_type < 0.3 THEN ' (m/f/x)' ELSE '' END AS job_title,
               'City ' || (i % 500) || ', ' || job_country AS job_location,
               CASE WHEN r_type < 0.5 THEN 'via LinkedIn' ELSE 'via BeBee' END AS job_via,
               CASE WHEN r_type < 0.8 THEN 'Full-time' ELSE 'Contractor' END AS job_schedule_type,
               (r_type > 0.9) AS job_work_from_home,
               job_country AS search_location,
               TIMESTAMP '2023-01-01' + INTERVAL (i % 365) DAY + INTERVAL (i % 86400) SECOND AS job_posted_date,
               (r_type > 0.85) AS job_no_degree_mention,
               (r_type < 0.1) AS job_health_insurance,
               job_country,
               CASE WHEN r_salary < 0.03 THEN 'year' WHEN r_salary < 0.05 THEN 'hour' END AS salary_rate,
               CASE WHEN r_salary < 0.03 THEN round(40000 + rnd(i, 7) * 120000, 0) END AS salary_year_avg,
               CASE WHEN r_salary >= 0.03 AND r_salary < 0.05 THEN round(15 + rnd(i, 8) * 80, 2) END AS salary_hour_avg,
               'Company ' || (i % 3000) AS company_name,
               CASE WHEN r_skills < 0.15 THEN NULL ELSE
                   '[' || array_to_string(list_transform(range(n_skills),
                       lambda x: '''' || {skills}[1 + (rnd(i * 16 + x, 9) * {len(SKILLS) - 1})::INT] || ''''), ', ') || ']'
               END AS job_skills,
               NULL::VARCHAR AS job_type_skills
        FROM base
    """)
    connection.sql(f"COPY postings TO '{SYNTHETIC_CSV.as_posix()}' (HEADER)")
    rows = connection.sql("SELECT count(*) FROM postings").fetchall()[0][0]
    print(f"CSV sintético: {SYNTHETIC_CSV} ({format_int(rows)} filas)")
    print("Son datos INVENTADOS: sirven para ensayar, no para sacar conclusiones.")


if __name__ == "__main__":
    main()
