# AI-Powered Automotive Data Quality & Auto-Cleaning System

## 1. Project Overview

The **AI-Powered Automotive Data Quality & Auto-Cleaning System** is a Python-based data analytics application designed to identify data quality issues, clean inconsistent automotive engineering-change records, and generate meaningful insights using Artificial Intelligence.

The application helps users analyze missing values, duplicate records, invalid entries, inconsistent categories, and quality-score issues. It also provides automated cleaning, manual review support, interactive dashboards, and an AI-powered chat assistant.

## 2. Project Objectives

- Identify data quality issues in automotive engineering-change data.
- Detect missing values, duplicates, invalid values, and inconsistent records.
- Automatically clean records wherever possible.
- Flag records that require manual verification.
- Compare data quality before and after cleaning.
- Generate AI-powered insights and answer questions about dataset statistics.

## 3. Key Features

### 3.1 Dashboard
- Displays key dataset metrics.
- Provides an overview of engineering-change records.
- Presents important data quality indicators.

### 3.2 Data Quality Analysis
- Identifies missing values.
- Detects duplicate records.
- Checks invalid dates and inconsistent values.
- Evaluates quality scores.

### 3.3 Data Cleaning
- Removes exact duplicate records.
- Standardizes inconsistent status values.
- Converts and validates date fields.
- Identifies invalid priorities and change types.
- Validates quality scores between 0 and 100.

### 3.4 Manual Review
- Flags records that require human verification.
- Identifies duplicate IDs and invalid or missing information.
- Allows users to download records requiring review.

### 3.5 AI-Powered Insights
- Generates insights using Google Gemini.
- Summarizes important dataset quality findings.
- Provides data-driven observations.

### 3.6 Before vs After Comparison
- Compares total records before and after cleaning.
- Compares missing values and duplicate records.
- Shows valid quality-score counts.
- Displays records requiring manual review.

### 3.7 AI Data Chat Assistant
- Allows users to ask questions about dataset statistics using natural language.
- Provides answers based on calculated dataset summaries.
- Maintains conversation history during the session.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data processing and cleaning |
| Streamlit | Interactive web application |
| Google Gemini API | AI-powered insights and chat |
| CSV | Dataset input and cleaned data export |

## 5. Dataset Information

The project uses an automotive engineering-change dataset containing the following fields:

- Change ID
- Part ID
- Part Name
- Change Type
- Request Date
- Due Date
- Status
- Priority
- Supplier
- Quality Score

**Note:** The sample dataset is synthetic and created for project demonstration and testing.

## 6. Installation and Execution

### Step 1: Download or Clone the Repository

Download the project files or clone the GitHub repository to your local system.

### Step 2: Install Dependencies

Open the terminal in the project directory and execute:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Gemini API Key

Create a `.env` file in the project directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Keep your API key private. Do not upload the `.env` file to GitHub.

### Step 4: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

### Step 5: Upload a CSV File

Upload an automotive engineering-change CSV dataset through the application sidebar and explore the available features.

## 7. Expected Outcomes

- Improved visibility into data quality issues.
- Reduced manual effort in identifying common data inconsistencies.
- Cleaner and more standardized datasets.
- Better identification of records requiring human review.
- Faster understanding of dataset quality through AI-generated insights.

## 8. Future Enhancements

- Support for additional automotive datasets.
- Advanced data validation rules.
- More detailed analytics and reporting.
- Integration with enterprise data sources.

## 9. Conclusion

This project demonstrates how Python, Pandas, Streamlit, and Generative AI can be combined to build a practical data quality analysis and auto-cleaning application for automotive engineering data.

It brings together data cleaning, validation, visualization, manual review, and AI-assisted insights in one interactive application.
