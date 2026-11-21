
import pandas as pd

df = pd.read_csv("engineering_changes.csv")

print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nExact duplicate rows:", df.duplicated().sum())

print("\nDuplicate change IDs:", df["change_id"].duplicated().sum())

print("\nInvalid request dates:",
      pd.to_datetime(df["request_date"], errors="coerce").isna().sum())

print("\nInvalid due dates:",
      pd.to_datetime(df["due_date"], errors="coerce").isna().sum())

print("\nStatus counts:")
print(df["status"].value_counts())

print("\nPriority counts:")
print(df["priority"].value_counts())

print("\nChange type counts:")
print(df["change_type"].value_counts())

print("\nInvalid quality scores:",
      ((df["quality_score"] < 1) |
       (df["quality_score"] > 100)).sum())
