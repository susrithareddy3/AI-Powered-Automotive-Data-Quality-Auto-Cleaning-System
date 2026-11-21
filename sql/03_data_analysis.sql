USE automotive_data_quality;

-- 1. Status-wise analysis
SELECT
    status,
    COUNT(*) AS total_changes
FROM engineering_changes
GROUP BY status
ORDER BY total_changes DESC;


-- 2. Priority-wise analysis
SELECT
    priority,
    COUNT(*) AS total_changes
FROM engineering_changes
GROUP BY priority
ORDER BY total_changes DESC;


-- 3. Status and priority analysis
SELECT
    priority,
    status,
    COUNT(*) AS total_changes
FROM engineering_changes
GROUP BY priority, status
ORDER BY priority, total_changes DESC;
-- 4. Missing values analysis
SELECT
    SUM(part_name IS NULL OR TRIM(part_name) = '') AS missing_part_names,
    SUM(supplier IS NULL OR TRIM(supplier) = '') AS missing_suppliers,
    SUM(quality_score IS NULL) AS missing_quality_scores,
    SUM(priority IS NULL OR TRIM(priority) = '') AS missing_priorities
FROM engineering_changes;


-- 5. Duplicate IDs and date issues
SELECT
    SUM(change_id_needs_review = 'True') AS duplicate_id_records,
    SUM(request_date_needs_review = 'True') AS invalid_request_dates,
    SUM(due_date_needs_review = 'True') AS invalid_due_dates,
    SUM(date_order_needs_review = 'True') AS incorrect_date_order
FROM engineering_changes;


-- 6. Supplier performance analysis
SELECT
    supplier,
    COUNT(*) AS total_changes,
    ROUND(AVG(quality_score), 2) AS avg_quality_score
FROM engineering_changes
GROUP BY supplier
ORDER BY total_changes DESC;
-- 7. Overall quality score analysis
SELECT
    ROUND(AVG(quality_score), 2) AS average_score,
    MAX(quality_score) AS highest_score,
    MIN(quality_score) AS lowest_score,
    COUNT(quality_score) AS valid_scores
FROM engineering_changes;


-- 8. Quality score categorization using CASE WHEN
SELECT
    change_id,
    quality_score,
    CASE
        WHEN quality_score IS NULL THEN 'Not Available'
        WHEN quality_score >= 80 THEN 'Good'
        WHEN quality_score >= 60 THEN 'Average'
        ELSE 'Poor'
    END AS quality_category
FROM engineering_changes;


-- 9. Suppliers above overall average quality
SELECT
    supplier,
    ROUND(AVG(quality_score), 2) AS avg_quality
FROM engineering_changes
WHERE supplier IS NOT NULL
  AND TRIM(supplier) <> ''
GROUP BY supplier
HAVING AVG(quality_score) > (
    SELECT AVG(quality_score)
    FROM engineering_changes
);


-- 10. Supplier summary using CTE
WITH supplier_summary AS (
    SELECT
        supplier,
        COUNT(*) AS total_changes,
        ROUND(AVG(quality_score), 2) AS avg_quality
    FROM engineering_changes
    WHERE supplier IS NOT NULL
      AND TRIM(supplier) <> ''
    GROUP BY supplier
)
SELECT *
FROM supplier_summary
ORDER BY avg_quality DESC;


-- 11. Supplier ranking using RANK()
WITH supplier_summary AS (
    SELECT
        supplier,
        ROUND(AVG(quality_score), 2) AS avg_quality
    FROM engineering_changes
    WHERE supplier IS NOT NULL
      AND TRIM(supplier) <> ''
    GROUP BY supplier
)
SELECT
    supplier,
    avg_quality,
    RANK() OVER (ORDER BY avg_quality DESC) AS supplier_rank
FROM supplier_summary;


-- 12. Row numbering using ROW_NUMBER()
SELECT
    change_id,
    supplier,
    quality_score,
    ROW_NUMBER() OVER (
        PARTITION BY supplier
        ORDER BY quality_score DESC
    ) AS row_num
FROM engineering_changes
WHERE supplier IS NOT NULL
  AND TRIM(supplier) <> '';