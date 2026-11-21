import hashlib
import io
import json
import os
import time

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors


# ---------------------------------------------------------
# PAGE CONFIGURATION AND STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Automotive Data Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #1F4E79;
            font-weight: 700;
        }
        h2, h3 {
            color: #245B83;
        }
        div[data-testid="stMetric"] {
            background-color: rgba(70, 130, 180, 0.08);
            padding: 16px;
            border-radius: 10px;
            border: 1px solid rgba(70, 130, 180, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
for key, default_value in {
    "cleaned_df": None,
    "quality_report": None,
    "ai_insights": None,
    "ai_chat_history": [],
    "file_hash": None,
    "source_file_name": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


# ---------------------------------------------------------
# SIDEBAR NAVIGATION AND FILE UPLOAD
# ---------------------------------------------------------
with st.sidebar:
    st.title("🚗 AutoData AI")
    st.caption("Automotive Data Intelligence Platform")
    st.divider()

    selected_page = st.radio(
        "Go to",
        [
            "Dashboard",
            "Data Quality Analysis",
            "Data Cleaning",
            "Manual Review",
            "AI Insights",
        ],
        key="selected_page",
    )

    st.divider()
    st.subheader("Dataset")
    uploaded_file = st.file_uploader(
        "Upload engineering changes CSV",
        type=["csv"],
        key="dataset_upload",
    )

    st.divider()
    st.caption("Built with Python, Pandas, Streamlit and Gemini AI.")


# ---------------------------------------------------------
# LOAD AND VALIDATE DATASET
# ---------------------------------------------------------
df = None

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.getvalue()

        if not file_bytes:
            st.error("The uploaded CSV file is empty.")
            st.stop()

        # Include the filename and file contents in the fingerprint.
        file_fingerprint = hashlib.sha256(
            uploaded_file.name.encode("utf-8") + file_bytes
        ).hexdigest()

        if st.session_state["file_hash"] != file_fingerprint:
            st.session_state["cleaned_df"] = None
            st.session_state["quality_report"] = None
            st.session_state["ai_insights"] = None
            st.session_state["ai_chat_history"] = []
            st.session_state["file_hash"] = file_fingerprint
            st.session_state["source_file_name"] = uploaded_file.name

        df = pd.read_csv(io.BytesIO(file_bytes))

        if df.empty:
            st.error("The CSV file has headers but contains no data rows.")
            df = None
        elif len(df.columns) == 0:
            st.error("The CSV file does not contain readable columns.")
            df = None

    except pd.errors.EmptyDataError:
        st.error("The uploaded file does not contain a valid CSV table.")
    except pd.errors.ParserError as error:
        st.error(f"Unable to parse the CSV file. Please check its format: {error}")
    except UnicodeDecodeError:
        st.error("The CSV encoding could not be read. Save the file as UTF-8 and upload it again.")
    except Exception as error:
        st.error(f"Unable to read the uploaded CSV file: {error}")


# ---------------------------------------------------------
# SHARED DATA CLEANING FUNCTION
# ---------------------------------------------------------
def clean_dataset(source_df):
    cleaned = source_df.copy()
    original_count = len(cleaned)

    # Remove exact duplicate rows.
    cleaned = cleaned.drop_duplicates().copy()
    duplicates_removed = original_count - len(cleaned)

    # Standardize status values.
    if "status" in cleaned.columns:
        status_map = {
            "in progress": "In Progress",
            "pending": "Pending",
            "completed": "Completed",
            "open": "Open",
        }
        cleaned["status"] = (
            cleaned["status"]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace(status_map)
        )

    # Convert date columns safely.
    for column in ["request_date", "due_date"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(
                cleaned[column],
                errors="coerce",
            )

    # Flag missing or non-standard change types.
    if "change_type" in cleaned.columns:
        valid_types = [
            "Design Update",
            "Material Change",
            "Supplier Change",
        ]
        change_type_values = cleaned["change_type"].astype("string").str.strip()
        cleaned["invalid_change_type_review"] = (
            change_type_values.isna()
            | ~change_type_values.isin(valid_types)
        )

    # Flag missing or non-standard priorities.
    if "priority" in cleaned.columns:
        valid_priorities = ["High", "Medium", "Low"]
        priority_values = cleaned["priority"].astype("string").str.strip()
        cleaned["invalid_priority_review"] = (
            priority_values.isna()
            | ~priority_values.isin(valid_priorities)
        )

    # Validate quality scores. Missing, non-numeric, and out-of-range
    # values are all sent for manual review.
    if "quality_score" in cleaned.columns:
        cleaned["quality_score"] = pd.to_numeric(
            cleaned["quality_score"],
            errors="coerce",
        )
        cleaned["invalid_quality_score_review"] = (
            ~cleaned["quality_score"].between(0, 100)
        )

    # Flag duplicate change IDs.
    if "change_id" in cleaned.columns:
        cleaned["duplicate_change_id_review"] = (
            cleaned["change_id"].duplicated(keep=False)
        )

    # Flag missing or invalid dates.
    if "request_date" in cleaned.columns:
        cleaned["invalid_request_date_review"] = (
            cleaned["request_date"].isna()
        )

    if "due_date" in cleaned.columns:
        cleaned["invalid_due_date_review"] = (
            cleaned["due_date"].isna()
        )

    # Flag due dates earlier than request dates.
    if {"request_date", "due_date"}.issubset(cleaned.columns):
        cleaned["date_order_review"] = (
            cleaned["request_date"].notna()
            & cleaned["due_date"].notna()
            & (cleaned["due_date"] < cleaned["request_date"])
        )

    # Flag missing part names.
    if "part_name" in cleaned.columns:
        cleaned["missing_part_name_review"] = (
            cleaned["part_name"].isna()
            | cleaned["part_name"].astype("string").str.strip().eq("").fillna(False)
        )

    # Flag missing supplier information.
    if "supplier" in cleaned.columns:
        cleaned["missing_supplier_review"] = (
            cleaned["supplier"].isna()
            | cleaned["supplier"].astype("string").str.strip().eq("").fillna(False)
        )

    # Calculate manual-review rows AFTER all review flags are created.
    review_columns = [
        column for column in cleaned.columns
        if column.endswith("_review")
    ]

    rows_for_review = (
        int(cleaned[review_columns].any(axis=1).sum())
        if review_columns
        else 0
    )

    report = pd.DataFrame(
        {
            "Metric": [
                "Original Records",
                "Exact Duplicates Removed",
                "Records After Cleaning",
                "Missing Values Remaining",
                "Rows Requiring Manual Review",
            ],
            "Count": [
                original_count,
                duplicates_removed,
                len(cleaned),
                int(cleaned.isnull().sum().sum()),
                rows_for_review,
            ],
        }
    )

    return cleaned, report


# ---------------------------------------------------------
# COMMON PAGE HEADER
# ---------------------------------------------------------
st.title("🚗 AI-Powered Automotive Data Quality & Auto-Cleaning System")

if df is None:
    st.info(
        "Upload an engineering changes CSV file using the sidebar "
        "to get started."
    )
    st.stop()

st.caption(f"Current dataset: {uploaded_file.name}")


# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------
if selected_page == "Dashboard":
    st.subheader("📊 Automotive Data Dashboard")
    st.write(
        "Welcome to AutoData AI — your automotive engineering "
        "data quality and intelligence platform."
    )

    total_records = len(df)
    total_columns = len(df.columns)
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records", total_records)
    col2.metric("Total Columns", total_columns)
    col3.metric("Missing Values", missing_values)
    col4.metric("Exact Duplicates", duplicate_rows)

    st.divider()
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), width="stretch")

    if "status" in df.columns:
        st.subheader("Engineering Change Status")
        status_counts = df["status"].value_counts(dropna=False)
        st.bar_chart(status_counts)


# ---------------------------------------------------------
# DATA QUALITY ANALYSIS PAGE
# ---------------------------------------------------------
elif selected_page == "Data Quality Analysis":
    st.subheader("📊 Data Quality Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), width="stretch")

    st.subheader("Missing Values Analysis")
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        missing_report = (
            missing.rename("Missing Count")
            .reset_index()
            .rename(columns={"index": "Column"})
        )
        st.dataframe(missing_report, width="stretch")
        st.bar_chart(missing)
    else:
        st.success("No missing values found!")

    st.subheader("Duplicate Records")
    st.metric("Exact Duplicate Rows", int(df.duplicated().sum()))


# ---------------------------------------------------------
# DATA CLEANING PAGE
# ---------------------------------------------------------
elif selected_page == "Data Cleaning":
    st.subheader("🧹 Automatic Data Cleaning")
    st.write("Run the cleaning process on the uploaded dataset.")

    if st.button("🧹 Auto-Clean Data", type="primary"):
        cleaned_df, quality_report = clean_dataset(df)
        st.session_state["cleaned_df"] = cleaned_df
        st.session_state["quality_report"] = quality_report
        st.session_state["ai_insights"] = None
        st.success("Data cleaning completed!")

    cleaned_df = st.session_state.get("cleaned_df")
    quality_report = st.session_state.get("quality_report")

    if cleaned_df is not None and quality_report is not None:
        st.subheader("Cleaning Results")

        report_values = dict(
            zip(quality_report["Metric"], quality_report["Count"])
        )
        metric_columns = st.columns(5)

        for metric_column, (metric, value) in zip(
            metric_columns,
            report_values.items(),
        ):
            metric_column.metric(metric, int(value))

        # -----------------------------------------------------
        # BEFORE VS AFTER CLEANING COMPARISON
        # -----------------------------------------------------
        st.divider()
        st.subheader("📊 Before vs After Cleaning Comparison")
        st.caption(
            "Compare the uploaded dataset with the cleaned dataset "
            "using the same quality checks."
        )

        # Original dataset statistics.
        before_records = len(df)
        before_missing = int(df.isnull().sum().sum())
        before_duplicates = int(df.duplicated().sum())

        # Cleaned dataset statistics.
        after_records = len(cleaned_df)
        after_missing = int(cleaned_df.isnull().sum().sum())
        after_duplicates = int(cleaned_df.duplicated().sum())

        # Count quality scores within the accepted 0–100 range.
        if "quality_score" in df.columns:
            before_scores = pd.to_numeric(
                df["quality_score"], errors="coerce"
            )
            before_valid_scores = int(
                before_scores.between(0, 100).sum()
            )
        else:
            before_valid_scores = "N/A"

        if "quality_score" in cleaned_df.columns:
            after_scores = pd.to_numeric(
                cleaned_df["quality_score"], errors="coerce"
            )
            after_valid_scores = int(
                after_scores.between(0, 100).sum()
            )
        else:
            after_valid_scores = "N/A"

        # Count records that have at least one manual-review flag.
        review_columns = [
            column for column in cleaned_df.columns
            if column.endswith("_review")
        ]
        after_review_rows = (
            int(cleaned_df[review_columns].any(axis=1).sum())
            if review_columns
            else 0
        )

        comparison_df = pd.DataFrame(
            {
                "Metric": [
                    "Total Records",
                    "Missing Values",
                    "Exact Duplicate Rows",
                    "Valid Quality Scores (0–100)",
                    "Rows Requiring Manual Review",
                ],
                "Before Cleaning": [
                    before_records,
                    before_missing,
                    before_duplicates,
                    before_valid_scores,
                    "Not applicable",
                ],
                "After Cleaning": [
                    after_records,
                    after_missing,
                    after_duplicates,
                    after_valid_scores,
                    after_review_rows,
                ],
            }
        )

        st.dataframe(comparison_df, hide_index=True, width="stretch")

        st.info(
            "Note: Missing values may remain or increase when invalid "
            "values are converted into missing values during validation. "
            "Rows requiring manual review are identified for human "
            "verification; they are not automatically treated as errors "
            "that can safely be corrected."
        )

        st.subheader("Cleaned Dataset Preview")
        st.dataframe(cleaned_df.head(10), width="stretch")

        st.download_button(
            "⬇️ Download Cleaned CSV",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_engineering_changes.csv",
            mime="text/csv",
        )

        st.download_button(
            "⬇️ Download Quality Report",
            data=quality_report.to_csv(index=False).encode("utf-8"),
            file_name="quality_report.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "Click 'Auto-Clean Data' to generate the cleaned dataset "
            "and quality report."
        )


# ---------------------------------------------------------
# MANUAL REVIEW PAGE
# ---------------------------------------------------------
elif selected_page == "Manual Review":
    st.subheader("🔍 Manual Review")

    cleaned_df = st.session_state.get("cleaned_df")

    if cleaned_df is None:
        st.info("Go to Data Cleaning and click 'Auto-Clean Data' first.")
    else:
        review_columns = [
            column for column in cleaned_df.columns
            if column.endswith("_review")
        ]

        if not review_columns:
            st.success("No manual-review flags were generated.")
        else:
            review_mask = cleaned_df[review_columns].any(axis=1)
            review_df = cleaned_df.loc[review_mask].copy()

            st.metric("Rows Requiring Manual Review", len(review_df))
            st.write(
                "Rows are shown when at least one review flag is True."
            )
            st.dataframe(review_df, width="stretch")

            st.download_button(
                "⬇️ Download Manual Review Records",
                data=review_df.to_csv(index=False).encode("utf-8"),
                file_name="manual_review_records.csv",
                mime="text/csv",
            )


# ---------------------------------------------------------
# AI INSIGHTS PAGE
# ---------------------------------------------------------
elif selected_page == "AI Insights":
    st.subheader("🤖 AI-Powered Data Insights")

    cleaned_df = st.session_state.get("cleaned_df")
    quality_report = st.session_state.get("quality_report")

    if cleaned_df is None or quality_report is None:
        st.info("Go to Data Cleaning and click 'Auto-Clean Data' first.")
    else:
        st.write(
            "Generate business-focused observations and recommendations "
            "from the cleaned automotive engineering dataset."
        )

        if st.button("Generate AI Insights", type="primary"):
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                st.error("Gemini API key not found. Check your .env file.")
            else:
                try:
                    client = genai.Client(api_key=api_key)

                    # Calculate dataset statistics.
                    def value_counts_if_present(column):
                        if column in cleaned_df.columns:
                            return cleaned_df[column].value_counts(
                                dropna=False
                            ).to_dict()
                        return "Column not available"

                    if "quality_score" in cleaned_df.columns:
                        scores = pd.to_numeric(
                            cleaned_df["quality_score"],
                            errors="coerce",
                        )
                        valid_score_mask = scores.between(0, 100)
                        valid_scores = scores[valid_score_mask]
                        quality_average = (
                            round(valid_scores.mean(), 2)
                            if not valid_scores.empty
                            else "No valid scores"
                        )
                        valid_score_count = int(valid_score_mask.sum())
                        invalid_or_missing_score_count = int(
                            (~valid_score_mask).sum()
                        )
                    else:
                        quality_average = "Column not available"
                        valid_score_count = "Column not available"
                        invalid_or_missing_score_count = "Column not available"

                    insights = {
                        "Total cleaned records": len(cleaned_df),
                        "Status distribution": value_counts_if_present("status"),
                        "Priority distribution": value_counts_if_present("priority"),
                        "Supplier distribution": value_counts_if_present("supplier"),
                        "Average valid quality score (0-100)": quality_average,
                        "Valid quality score count": valid_score_count,
                        "Missing or invalid quality score count": (
                            invalid_or_missing_score_count
                        ),
                        "Missing values by column": (
                            cleaned_df.isnull().sum().to_dict()
                        ),
                        "Cleaning summary": quality_report.to_dict(
                            orient="records"
                        ),
                    }

                    # Prepare Gemini prompt.
                    prompt = f"""
You are an automotive data analytics expert.

Analyze this synthetic automotive engineering change dataset.

DATA:
{insights}

Provide the following sections:
1. Overall dataset summary.
2. Status and priority observations.
3. Supplier observations.
4. Quality score analysis.
5. Potential business risks.
6. Three actionable recommendations.

Rules:
- Use only the supplied statistics.
- Do not invent numbers.
- Do not claim supplier performance without supporting performance metrics.
- Mention when information is insufficient.
- Distinguish missing values from rows requiring review.
- Do not assume that all non-completed records are delayed.
- Quality scores are valid only from 0 to 100.
- Use simple professional business language.
"""

                    response = None
                    last_api_error = None

                    with st.spinner("AI is analyzing your dataset..."):
                        for attempt in range(3):
                            try:
                                response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=prompt,
                                )
                                break
                            except errors.APIError as error:
                                last_api_error = error

                                if error.code == 503 and attempt < 2:
                                    time.sleep(2 ** (attempt + 1))
                                else:
                                    break

                    if response is not None and response.text:
                        st.session_state["ai_insights"] = response.text
                        st.success("AI analysis completed!")
                    elif last_api_error is not None:
                        st.error(
                            "Gemini could not complete the request: "
                            f"{last_api_error}"
                        )
                    else:
                        st.warning(
                            "Gemini returned an empty response. "
                            "Please try again."
                        )

                except Exception as error:
                    st.error(f"AI analysis failed: {error}")

        # Display previously generated insights.
        saved_insights = st.session_state.get("ai_insights")

        if saved_insights:
            st.divider()
            st.markdown(saved_insights)

        # -----------------------------------------------------
        # AI DATA CHAT ASSISTANT
        # -----------------------------------------------------
        st.divider()
        st.subheader("💬 Ask Questions About Your Dataset")
        st.caption(
            "Ask questions about the cleaned dataset. Answers are based "
            "on calculated dataset statistics, not assumptions."
        )

        for chat_message in st.session_state["ai_chat_history"]:
            with st.chat_message(chat_message["role"]):
                st.markdown(chat_message["content"])

        user_question = st.chat_input(
            "Example: Which priority has the most engineering changes?"
        )

        if user_question:
            st.session_state["ai_chat_history"].append(
                {"role": "user", "content": user_question}
            )

            with st.chat_message("user"):
                st.markdown(user_question)

            chat_data_summary = {
                "total_records": int(len(cleaned_df)),
                "columns": list(cleaned_df.columns),
                "missing_values_by_column": {
                    str(column): int(count)
                    for column, count in cleaned_df.isnull().sum().items()
                },
                "total_missing_values": int(cleaned_df.isnull().sum().sum()),
                "exact_duplicate_rows": int(cleaned_df.duplicated().sum()),
            }

            for column in ["status", "priority", "change_type", "supplier"]:
                if column in cleaned_df.columns:
                    counts = cleaned_df[column].value_counts(
                        dropna=False
                    ).head(20)
                    chat_data_summary[f"{column}_counts"] = {
                        str(key): int(value) for key, value in counts.items()
                    }

            if "quality_score" in cleaned_df.columns:
                scores = pd.to_numeric(
                    cleaned_df["quality_score"], errors="coerce"
                )
                valid_scores = scores[scores.between(0, 100)]
                chat_data_summary["quality_score"] = {
                    "valid_score_count": int(len(valid_scores)),
                    "missing_or_invalid_count": int((~scores.between(0, 100)).sum()),
                    "average_valid_score": (
                        round(float(valid_scores.mean()), 2)
                        if not valid_scores.empty else None
                    ),
                    "minimum_valid_score": (
                        round(float(valid_scores.min()), 2)
                        if not valid_scores.empty else None
                    ),
                    "maximum_valid_score": (
                        round(float(valid_scores.max()), 2)
                        if not valid_scores.empty else None
                    ),
                }

            review_columns_for_chat = [
                column for column in cleaned_df.columns
                if column.endswith("_review")
            ]
            chat_data_summary["rows_requiring_manual_review"] = (
                int(cleaned_df[review_columns_for_chat].any(axis=1).sum())
                if review_columns_for_chat else 0
            )

            chat_prompt = f"""
You are a careful automotive data analytics assistant.
Answer using ONLY the dataset summary below. Never invent values,
records, trends, causes, or business facts. If the summary is insufficient,
say so clearly. Do not claim supplier performance without supporting
metrics. Do not assume non-completed records are delayed. Quality scores
are valid only from 0 to 100. Use simple professional language.

DATASET SUMMARY:
{json.dumps(chat_data_summary, default=str, indent=2)}

USER QUESTION:
{user_question}
"""

            load_dotenv()
            chat_api_key = os.getenv("GEMINI_API_KEY")

            with st.chat_message("assistant"):
                if not chat_api_key:
                    assistant_answer = (
                        "Gemini API key not found. Please check your .env file."
                    )
                    st.error(assistant_answer)
                else:
                    try:
                        chat_client = genai.Client(api_key=chat_api_key)
                        with st.spinner("Analyzing your question..."):
                            chat_response = chat_client.models.generate_content(
                                model="gemini-3.5-flash-lite",
                                contents=chat_prompt,
                            )

                        if chat_response is not None and chat_response.text:
                            assistant_answer = chat_response.text
                            st.markdown(assistant_answer)
                        else:
                            assistant_answer = (
                                "I couldn't generate an answer. Please try "
                                "asking the question differently."
                            )
                            st.warning(assistant_answer)
                    except errors.APIError as error:
                        assistant_answer = (
                            f"Gemini could not answer this question: {error}"
                        )
                        st.error(assistant_answer)
                    except Exception as error:
                        assistant_answer = f"Unable to process this question: {error}"
                        st.error(assistant_answer)

            st.session_state["ai_chat_history"].append(
                {"role": "assistant", "content": assistant_answer}
            )
