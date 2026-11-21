# AI-Powered Automotive Data Quality & Auto-Cleaning System

## Project Overview

The **AI-Powered Automotive Data Quality & Auto-Cleaning System** is a Python-based data analytics application designed to identify data quality issues, clean inconsistent automotive engineering-change records, and generate meaningful insights using AI.

The application helps users analyze missing values, duplicate records, invalid entries, inconsistent categories, and quality-score issues. It also provides automated cleaning, manual review support, interactive dashboards, and an AI-powered chat assistant.

## Objectives

- Identify data quality issues in automotive engineering-change data.
- Detect missing values, duplicates, invalid values, and inconsistent records.
- Automatically clean records where possible.
- Flag records that require manual verification.
- Compare data quality before and after cleaning.
- Generate AI-powered insights and answer questions about dataset statistics.

## Key Features

### 1. Dashboard
- Displays key dataset metrics.
- Provides an overview of engineering-change records.
- Presents important data quality indicators.

### 2. Data Quality Analysis
- Identifies missing values.
- Detects duplicate records.
- Checks invalid dates and inconsistent values.
- Evaluates quality scores.

### 3. Data Cleaning
- Removes exact duplicate records.
- Standardizes inconsistent status values.
- Converts and validates date fields.
- Identifies invalid priorities and change types.
- Validates quality scores between 0 and 100.

### 4. Manual Review
- Flags records that require human verification.
- Identifies duplicate IDs and invalid or missing information.
- Allows users to download records requiring review.

### 5. AI-Powered Insights
- Generates insights using Google Gemini.
- Summarizes important dataset quality findings.
- Provides data-driven observations.

### 6. Before vs After Comparison
- Compares total records before and after cleaning.
- Compares missing values and duplicate records.
- Shows valid quality-score counts.
- Displays records requiring manual review.

### 7. AI Data Chat Assistant
- Allows users to ask questions about dataset statistics using natural language.
- Provides answers based on calculated dataset summaries.
- Maintains conversation history during the session.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data processing and cleaning |
| Streamlit | Interactive web application |
| Google Gemini API | AI-powered insights and chat |
| CSV | Dataset input and cleaned data export |

## Dataset Information

The project uses an automotive engineering-change dataset containing fields such as:

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

The sample dataset is synthetic and created for project demonstration and testing.

## Installation and Execution

### 1. Clone or download the project

Download the project files to your local system.

### 2. Install dependencies

```bash
pip install streamlit pandas python-dotenv google-generativeai
```

Use the dependency versions from your project's requirements file if one is available.

### 3. Configure the Gemini API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not share or upload your actual API key.

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Upload a CSV file

Upload an automotive engineering-change CSV dataset through the application sidebar and explore the available pages.

## Expected Outcomes

- Improved visibility into data quality issues.
- Reduced manual effort in identifying common data inconsistencies.
- Cleaner and more standardized datasets.
- Better identification of records requiring human review.
- Faster understanding of dataset quality through AI-generated insights.

## Future Enhancements

- Support for additional automotive datasets.
- Advanced data validation rules.
- More detailed analytics and reporting.
- Integration with enterprise data sources.

## Conclusion

This project demonstrates how Python, Pandas, Streamlit, and Generative AI can be combined to build a practical data quality analysis and auto-cleaning application for automotive engineering data.

It brings together data cleaning, validation, visualization, manual review, and AI-assisted insights in one interactive application.# AI-Powered Automotive Data Quality & Auto-Cleaning System

## Project Overview

The **AI-Powered Automotive Data Quality & Auto-Cleaning System** is a Python-based data analytics application designed to identify data quality issues, clean inconsistent automotive engineering-change records, and generate meaningful insights using AI.

The application helps users analyze missing values, duplicate records, invalid entries, inconsistent categories, and quality-score issues. It also provides automated cleaning, manual review support, interactive dashboards, and an AI-powered chat assistant.

## Objectives

- Identify data quality issues in automotive engineering-change data.
- Detect missing values, duplicates, invalid values, and inconsistent records.
- Automatically clean records where possible.
- Flag records that require manual verification.
- Compare data quality before and after cleaning.
- Generate AI-powered insights and answer questions about dataset statistics.

## Key Features

### 1. Dashboard
- Displays key dataset metrics.
- Provides an overview of engineering-change records.
- Presents important data quality indicators.

### 2. Data Quality Analysis
- Identifies missing values.
- Detects duplicate records.
- Checks invalid dates and inconsistent values.
- Evaluates quality scores.

### 3. Data Cleaning
- Removes exact duplicate records.
- Standardizes inconsistent status values.
- Converts and validates date fields.
- Identifies invalid priorities and change types.
- Validates quality scores between 0 and 100.

### 4. Manual Review
- Flags records that require human verification.
- Identifies duplicate IDs and invalid or missing information.
- Allows users to download records requiring review.

### 5. AI-Powered Insights
- Generates insights using Google Gemini.
- Summarizes important dataset quality findings.
- Provides data-driven observations.

### 6. Before vs After Comparison
- Compares total records before and after cleaning.
- Compares missing values and duplicate records.
- Shows valid quality-score counts.
- Displays records requiring manual review.

### 7. AI Data Chat Assistant
- Allows users to ask questions about dataset statistics using natural language.
- Provides answers based on calculated dataset summaries.
- Maintains conversation history during the session.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data processing and cleaning |
| Streamlit | Interactive web application |
| Google Gemini API | AI-powered insights and chat |
| CSV | Dataset input and cleaned data export |

## Dataset Information

The project uses an automotive engineering-change dataset containing fields such as:

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

The sample dataset is synthetic and created for project demonstration and testing.

## Installation and Execution

### 1. Clone or download the project

Download the project files to your local system.

### 2. Install dependencies

```bash
pip install streamlit pandas python-dotenv google-generativeai
```

Use the dependency versions from your project's requirements file if one is available.

### 3. Configure the Gemini API key

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not share or upload your actual API key.

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Upload a CSV file

Upload an automotive engineering-change CSV dataset through the application sidebar and explore the available pages.

## Expected Outcomes

- Improved visibility into data quality issues.
- Reduced manual effort in identifying common data inconsistencies.
- Cleaner and more standardized datasets.
- Better identification of records requiring human review.
- Faster understanding of dataset quality through AI-generated insights.

## Future Enhancements

- Support for additional automotive datasets.
- Advanced data validation rules.
- More detailed analytics and reporting.
- Integration with enterprise data sources.

## Conclusion

This project demonstrates how Python, Pandas, Streamlit, and Generative AI can be combined to build a practical data quality analysis and auto-cleaning application for automotive engineering data.

It brings together data cleaning, validation, visualization, manual review, and AI-assisted insights in one interactive application.