-- TRAP 3. An average without its n misleads: almost no posting has a salary.
SELECT
    count(*)                                            AS total_postings,
    count(salary_year_avg)                              AS postings_with_yearly_salary,
    round(100.0 * count(salary_year_avg) / count(*), 1) AS pct_with_salary,
    round(avg(salary_year_avg))                         AS mean_salary,
    round(quantile_cont(salary_year_avg, 0.5))          AS median_salary
FROM jobs;
