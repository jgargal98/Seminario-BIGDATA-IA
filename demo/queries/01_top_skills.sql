-- Q1. Which skills are most requested in Data Engineer postings?
-- Base: Data Engineer postings that LIST skills.
-- job_skills is Python-style list TEXT, so it is parsed into a real list first.
-- Each skill counts ONCE per posting: some postings repeat a skill.
WITH base AS (
    SELECT row_id, job_skills
    FROM jobs
    WHERE job_title_short = 'Data Engineer'
      AND job_skills IS NOT NULL
),
skills AS (
    SELECT DISTINCT
           row_id,
           unnest(from_json(replace(job_skills, '''', '"'), '["VARCHAR"]')) AS skill
    FROM base
)
SELECT skill,
       count(*)                                                 AS postings,
       round(100.0 * count(*) / (SELECT count(*) FROM base), 1) AS pct_postings
FROM skills
GROUP BY skill
ORDER BY postings DESC, skill
LIMIT 15;
