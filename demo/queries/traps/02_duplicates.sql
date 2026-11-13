-- TRAP 2. Some postings list the same skill more than once.
-- Counting mentions is not the same as counting postings.
WITH exploded AS (
    SELECT row_id,
           unnest(from_json(replace(job_skills, '''', '"'), '["VARCHAR"]')) AS skill
    FROM jobs
    WHERE job_skills IS NOT NULL
)
SELECT
    count(*)                    AS mentions,
    count(DISTINCT (row_id, skill)) AS distinct_posting_skill_pairs,
    count(*) - count(DISTINCT (row_id, skill)) AS repeated_mentions
FROM exploded;
