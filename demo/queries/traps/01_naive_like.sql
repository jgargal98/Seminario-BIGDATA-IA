-- TRAP 1. job_skills is TEXT, not a list: LIKE matches substrings.
-- '%sql%' also matches nosql, mysql, postgresql, sql server...
-- '%r%' matches almost anything (python, power bi, airflow...).
SELECT
    count(*) FILTER (WHERE job_skills LIKE '%sql%')                        AS sql_naive,
    count(*) FILTER (WHERE list_contains(
        from_json(replace(job_skills, '''', '"'), '["VARCHAR"]'), 'sql'))  AS sql_parsed,
    count(*) FILTER (WHERE job_skills LIKE '%r%')                          AS r_naive,
    count(*) FILTER (WHERE list_contains(
        from_json(replace(job_skills, '''', '"'), '["VARCHAR"]'), 'r'))    AS r_parsed,
    count(job_skills)                                                      AS postings_with_skills
FROM jobs;
