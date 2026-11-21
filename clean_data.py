
import pandas as pd

# Load the original dataset
df = pd.read_csv("engineering_changes.csv")

# Keep a separate working copy
cleaned_df = df.copy()

print("Original dataset shape:", df.shape)
print("Working copy shape:", cleaned_df.shape)

print("\nInitial missing values:")
print(cleaned_df.isnull().sum())

print("\nInitial exact duplicate rows:",
      cleaned_df.duplicated().sum())

# Step 1: Remove exact duplicate rows
duplicates_before = cleaned_df.duplicated().sum()

cleaned_df = cleaned_df.drop_duplicates()

duplicates_removed = duplicates_before - cleaned_df.duplicated().sum()

print("\nExact duplicate rows found:", duplicates_before)
print("Rows after removing duplicates:", len(cleaned_df))
print("Exact duplicate rows removed:", duplicates_removed)

# Step 2: Standardize text values

# Fix status formatting
cleaned_df["status"] = cleaned_df["status"].replace({
    "in progress": "In Progress",
    "IN PROGRESS": "In Progress"
})

# Standardize surrounding spaces in text columns
text_columns = [
    "part_name", "change_type", "status",
    "priority", "supplier"
]

for column in text_columns:
    cleaned_df[column] = cleaned_df[column].apply(
        lambda value: value.strip() if isinstance(value, str) else value
    )

print("\nStatus counts after standardization:")
print(cleaned_df["status"].value_counts())

# Step 3: Validate date columns

for column in ["request_date", "due_date"]:
    cleaned_df[column] = pd.to_datetime(
        cleaned_df[column],
        errors="coerce"
    )

print("\nInvalid request dates:",
      cleaned_df["request_date"].isna().sum())

print("Invalid due dates:",
      cleaned_df["due_date"].isna().sum())

# Flag due dates earlier than request dates
invalid_date_order = (
    cleaned_df["request_date"].notna()
    & cleaned_df["due_date"].notna()
    & (cleaned_df["due_date"] < cleaned_df["request_date"])
)

print("Due dates before request dates:",
      invalid_date_order.sum())

# Step 4: Flag records with missing values

cleaned_df["part_name_missing"] = cleaned_df["part_name"].isna()
cleaned_df["supplier_missing"] = cleaned_df["supplier"].isna()
cleaned_df["quality_score_missing"] = cleaned_df["quality_score"].isna()

print("\nMissing-value review summary:")
print("Missing part names:",
      cleaned_df["part_name_missing"].sum())
print("Missing suppliers:",
      cleaned_df["supplier_missing"].sum())
print("Missing quality scores:",
      cleaned_df["quality_score_missing"].sum())

# Step 5: Validate quality scores and categories

# Quality score must be between 1 and 100
invalid_quality_score = (
    cleaned_df["quality_score"].notna()
    & (
        (cleaned_df["quality_score"] < 1)
        | (cleaned_df["quality_score"] > 100)
    )
)

# Check allowed priority values
valid_priorities = ["High", "Medium", "Low"]

invalid_priority = ~cleaned_df["priority"].isin(
    valid_priorities
)

# Check allowed change types
valid_change_types = [
    "Design Update",
    "Supplier Change",
    "Material Change"
]

invalid_change_type = ~cleaned_df["change_type"].isin(
    valid_change_types
)

print("\nInvalid quality scores:",
      invalid_quality_score.sum())

print("Invalid priorities:",
      invalid_priority.sum())

print("Invalid change types:",
      invalid_change_type.sum())

# Step 6: Standardize invalid categories safely

# Correct known status formatting variations
cleaned_df["status"] = cleaned_df["status"].replace({
    "in progress": "In Progress",
    "IN PROGRESS": "In Progress"
})

# Normalize text casing and whitespace for categories
cleaned_df["priority"] = cleaned_df["priority"].apply(
    lambda value: value.strip().title()
    if isinstance(value, str) else value
)

cleaned_df["change_type"] = cleaned_df["change_type"].apply(
    lambda value: value.strip().title()
    if isinstance(value, str) else value
)

# Map known invalid labels to missing values for review
cleaned_df["priority"] = cleaned_df["priority"].replace({
    "Urgent!!": pd.NA
})

cleaned_df["change_type"] = cleaned_df["change_type"].replace({
    "Unknown Type": pd.NA
})

print("\nPriority values after cleaning:")
print(cleaned_df["priority"].value_counts(dropna=False))

print("\nChange type values after cleaning:")
print(cleaned_df["change_type"].value_counts(dropna=False))

# Step 7: Flag invalid quality scores for review

invalid_quality_score = (
    cleaned_df["quality_score"].notna()
    & (
        (cleaned_df["quality_score"] < 1)
        | (cleaned_df["quality_score"] > 100)
    )
)

invalid_quality_count = invalid_quality_score.sum()

cleaned_df.loc[
    invalid_quality_score, "quality_score"
] = pd.NA

print("\nInvalid quality scores flagged:", invalid_quality_count)
print("Missing quality scores after cleaning:",
      cleaned_df["quality_score"].isna().sum())

# Step 8: Create date issue flags

invalid_request_date = cleaned_df["request_date"].isna()
invalid_due_date = cleaned_df["due_date"].isna()

due_before_request = (
    cleaned_df["request_date"].notna()
    & cleaned_df["due_date"].notna()
    & (cleaned_df["due_date"] < cleaned_df["request_date"])
)

cleaned_df["request_date_needs_review"] = invalid_request_date
cleaned_df["due_date_needs_review"] = invalid_due_date
cleaned_df["date_order_needs_review"] = due_before_request

print("\nDate review summary:")
print("Invalid request dates:", invalid_request_date.sum())
print("Invalid due dates:", invalid_due_date.sum())
print("Due dates before request dates:", due_before_request.sum())

# Step 9: Flag duplicate change IDs for review

duplicate_change_id = cleaned_df["change_id"].duplicated(
    keep=False
)

cleaned_df["change_id_needs_review"] = duplicate_change_id

print("\nDuplicate change ID review:")
print(
    "Rows with duplicate change IDs:",
    duplicate_change_id.sum()
)

print(
    "\nSample duplicate change ID records:"
)

print(
    cleaned_df.loc[
        duplicate_change_id,
        ["change_id", "part_id", "part_name", "status"]
    ].head(10)
)

# Step 10: Refresh review flags

cleaned_df["part_name_missing"] = cleaned_df["part_name"].isna()
cleaned_df["supplier_missing"] = cleaned_df["supplier"].isna()
cleaned_df["quality_score_missing"] = cleaned_df["quality_score"].isna()

cleaned_df["priority_needs_review"] = cleaned_df["priority"].isna()
cleaned_df["change_type_needs_review"] = cleaned_df["change_type"].isna()

# Refresh date flags
cleaned_df["request_date_needs_review"] = cleaned_df["request_date"].isna()
cleaned_df["due_date_needs_review"] = cleaned_df["due_date"].isna()

cleaned_df["date_order_needs_review"] = (
    cleaned_df["request_date"].notna()
    & cleaned_df["due_date"].notna()
    & (cleaned_df["due_date"] < cleaned_df["request_date"])
)

# Refresh duplicate change ID flags
cleaned_df["change_id_needs_review"] = (
    cleaned_df["change_id"].duplicated(keep=False)
)

print("\nFinal review flags:")
review_columns = [
    "part_name_missing",
    "supplier_missing",
    "quality_score_missing",
    "priority_needs_review",
    "change_type_needs_review",
    "request_date_needs_review",
    "due_date_needs_review",
    "date_order_needs_review",
    "change_id_needs_review"
]

for column in review_columns:
    print(f"{column}: {cleaned_df[column].sum()}")

# Step 11: Save cleaned dataset
cleaned_df.to_csv("cleaned_engineering_changes.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Final dataset shape:", cleaned_df.shape)

# Step 12: Create a separate quality report
quality_report = pd.DataFrame({
    "Issue": [
        "Exact duplicate rows removed",
        "Rows with missing part names",
        "Rows with missing suppliers",
        "Rows with missing quality scores",
        "Rows with invalid priorities",
        "Rows with invalid change types",
        "Rows with invalid request dates",
        "Rows with invalid due dates",
        "Rows with due dates before request dates",
        "Rows with duplicate change IDs"
    ],
    "Count": [
        duplicates_removed,
        cleaned_df["part_name_missing"].sum(),
        cleaned_df["supplier_missing"].sum(),
        cleaned_df["quality_score_missing"].sum(),
        cleaned_df["priority_needs_review"].sum(),
        cleaned_df["change_type_needs_review"].sum(),
        cleaned_df["request_date_needs_review"].sum(),
        cleaned_df["due_date_needs_review"].sum(),
        cleaned_df["date_order_needs_review"].sum(),
        cleaned_df["change_id_needs_review"].sum()
    ]
})

quality_report.to_csv("quality_report.csv", index=False)

print("\nQuality report saved successfully!")
print(quality_report.to_string(index=False))

# Step 13: Validate exported files

saved_df = pd.read_csv("cleaned_engineering_changes.csv")
saved_report = pd.read_csv("quality_report.csv")

print("\n--- Export Validation ---")

print("Cleaned file shape:", saved_df.shape)
print("Quality report shape:", saved_report.shape)

print(
    "Exact duplicate rows in cleaned file:",
    saved_df.duplicated().sum()
)

print(
    "Missing part names:",
    saved_df["part_name"].isna().sum()
)

print(
    "Missing suppliers:",
    saved_df["supplier"].isna().sum()
)

print(
    "Missing quality scores:",
    saved_df["quality_score"].isna().sum()
)

print("\nQuality report preview:")
print(saved_report.to_string(index=False))
