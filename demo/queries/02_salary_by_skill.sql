-- Q2. Which skills go with higher yearly salaries in Data Engineer postings?
-- Only a small minority of postings has a salary, so n is ALWAYS reported.
-- Median instead of mean (outliers), and skills with fewer than 30 salaried postings are dropped.
WITH base AS (
    SELECT row_id, job_skills, salary_year_avg
    FROM jobs
    WHERE job_title_short = 'Data Engineer'
      AND job_skills IS NOT NULL
      AND salary_year_avg IS NOT NULL
),
skills AS (
    SELECT DISTINCT
           row_id,
           salary_year_avg,
           unnest(from_json(replace(job_skills, '''', '"'), '["VARCHAR"]')) AS skill
    FROM base
)
SELECT skill,
       count(*)                                   AS salaried_postings,
       round(quantile_cont(salary_year_avg, 0.5)) AS median_salary
FROM skills
GROUP BY skill
HAVING count(*) >= 30
ORDER BY median_salary DESC, skill
LIMIT 15;
