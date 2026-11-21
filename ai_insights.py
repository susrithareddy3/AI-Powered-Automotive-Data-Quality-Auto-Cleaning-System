
import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

# Load datasets
df = pd.read_csv("cleaned_engineering_changes.csv")
report = pd.read_csv("quality_report.csv")

# Calculate actual dataset insights
insights = {
    "Total cleaned records": len(df),

    "Status distribution": (
        df["status"].fillna("Missing").value_counts().to_dict()
    ),

    "Priority distribution": (
        df["priority"].fillna("Missing").value_counts().to_dict()
    ),

    "Supplier-wise change count": (
        df["supplier"].fillna("Missing").value_counts().to_dict()
    ),

    "Average quality score": round(df["quality_score"].mean(), 2),

    "Average quality score by supplier": (
        df.assign(supplier=df["supplier"].fillna("Missing"))
        .groupby("supplier")["quality_score"]
        .mean()
        .round(2)
        .to_dict()
    ),

    "Missing values": (
        df.isnull().sum().to_dict()
    ),

    "Quality report": report.to_dict(orient="records")
}

# Connect to Gemini
client = genai.Client(api_key=api_key)

prompt = f"""
You are an automotive data analytics expert.

Analyze these statistics from a synthetic automotive
engineering change dataset.

DATA INSIGHTS:
{insights}

Provide:

1. Overall dataset overview.
2. Important patterns in status and priority.
3. Supplier-wise observations.
4. Quality score observations.
5. Business risks and areas needing attention.
6. Three actionable recommendations.

Rules:
- Use only the supplied statistics.
- Do not invent numbers or patterns.
- Analyze the current cleaned dataset, not the original dataset.
- Do not claim that removed duplicate rows still exist.
- Clearly mention when information is insufficient.
- Use simple professional language.
"""

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)

print("\n========== AI AUTOMOTIVE DATA INSIGHTS ==========\n")
print(response.text)
