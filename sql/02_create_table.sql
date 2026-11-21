USE automotive_data_quality;

DROP TABLE IF EXISTS engineering_changes;

CREATE TABLE engineering_changes (
    change_id VARCHAR(20),
    part_id VARCHAR(20),
    part_name VARCHAR(100),
    change_type VARCHAR(50),
    request_date DATE,
    due_date DATE,
    status VARCHAR(30),
    priority VARCHAR(20),
    supplier VARCHAR(100),
    quality_score DECIMAL(5,2),
    part_name_missing VARCHAR(5),
    supplier_missing VARCHAR(5),
    quality_score_missing VARCHAR(5),
    request_date_needs_review VARCHAR(5),
    due_date_needs_review VARCHAR(5),
    date_order_needs_review VARCHAR(5),
    change_id_needs_review VARCHAR(5),
    priority_needs_review VARCHAR(5),
    change_type_needs_review VARCHAR(5)
);
