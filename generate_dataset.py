
import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

parts = [
    "Brake Disc", "Wheel Bearing", "Steering Gear",
    "Air Filter", "Clutch Plate", "Oil Pump",
    "Drive Shaft", "Engine Mount", "Radiator",
    "Brake Pad", "Fuel Injector", "Gearbox",
    "Shock Absorber", "Water Pump", "Alternator"
]

change_types = [
    "Design Update", "Supplier Change", "Material Change"
]
statuses = ["Open", "In Progress", "Completed", "Pending"]
priorities = ["High", "Medium", "Low"]
suppliers = [
    "Supplier A", "Supplier B", "Supplier C",
    "Supplier D", "Supplier E"
]

start_date = date(2026, 1, 1)
end_date = date(2026, 10, 29)
date_range = (end_date - start_date).days

records = []

for i in range(1, 501):
    request_date = start_date + timedelta(
        days=random.randint(0, date_range)
    )
    due_date = request_date + timedelta(
        days=random.randint(7, 45)
    )

    records.append({
        "change_id": f"EC{i:04d}",
        "part_id": f"P{random.randint(1, 100):03d}",
        "part_name": random.choice(parts),
        "change_type": random.choice(change_types),
        "request_date": request_date.isoformat(),
        "due_date": due_date.isoformat(),
        "status": random.choice(statuses),
        "priority": random.choice(priorities),
        "supplier": random.choice(suppliers),
        "quality_score": random.randint(50, 100)
    })

df = pd.DataFrame(records)

# 1. Missing values
for row in random.sample(range(500), 35):
    df.loc[row, "part_name"] = None

for row in random.sample(range(500), 20):
    df.loc[row, "supplier"] = None

for row in random.sample(range(500), 15):
    df.loc[row, "quality_score"] = None

# 2. Invalid dates
for row in random.sample(range(500), 20):
    df.loc[row, "due_date"] = "not_available"

# 3. Inconsistent status formatting
for row in random.sample(range(500), 25):
    df.loc[row, "status"] = "in progress"

# 4. Invalid quality scores
for row in random.sample(range(500), 15):
    df.loc[row, "quality_score"] = random.choice([-10, 0, 120, 150])

# 5. Invalid categories
for row in random.sample(range(500), 15):
    df.loc[row, "priority"] = "Urgent!!"

for row in random.sample(range(500), 12):
    df.loc[row, "change_type"] = "unknown type"

# 6. Invalid request dates
for row in random.sample(range(500), 10):
    df.loc[row, "request_date"] = "invalid_date"

# 7. Due date earlier than request date
for row in random.sample(range(500), 15):
    df.loc[row, "due_date"] = (
        date(2025, 12, 1).isoformat()
    )

# 8. Duplicate change IDs
for row in random.sample(range(500), 12):
    target = random.choice([i for i in range(500) if i != row])
    df.loc[row, "change_id"] = df.loc[target, "change_id"]

# 9. Exact duplicate records
df = pd.concat(
    [df, df.sample(n=15, random_state=42)],
    ignore_index=True
)

df.to_csv("engineering_changes.csv", index=False)

print("Dataset generated successfully!")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("\nFirst 5 records:")
print(df.head())
print("\nCSV saved as engineering_changes.csv")
