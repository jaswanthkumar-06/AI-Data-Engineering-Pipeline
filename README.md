# AI Data Engineering Pipeline with Machine Learning Dashboard

An end-to-end data engineering project that integrates Python, Apache Airflow, PostgreSQL, dbt, scikit-learn, Streamlit, and Docker to process food delivery data, transform datasets, analyze customer reviews, and visualize business insights.

**Author:** Jaswanth Kumar Kommoju

[GitHub](https://github.com/jaswanthkumar-06) | [LinkedIn](https://www.linkedin.com/in/jaswanthkumar06) | [Portfolio](https://jaswanthkumar-06.github.io/my-portfolio/) | [Email](mailto:jeswanthkumarkommuji@gmail.com)

---

## Project Overview

This project simulates a food delivery analytics platform that generates synthetic customer, restaurant, order, food item, and review data. The data engineering workflow coordinates processing tasks, stores data in PostgreSQL, transforms datasets with dbt, and presents analytical insights through an interactive dashboard.

The project also includes customer review sentiment analysis and a scikit-learn classification workflow for experimenting with text-based sentiment prediction.

## Architecture

```text
Synthetic Data Generation
          |
          v
    Python Processing
          |
          v
     Apache Airflow
          |
          v
       PostgreSQL
          |
          v
       dbt Models
          |
          v
 Analytics and Sentiment
          |
          v
 Streamlit Dashboard
          |
          v
  Business Insights
```

## Key Features

- **Synthetic Data Generation:** Creates food delivery datasets for customers, restaurants, food items, orders, order items, and reviews.
- **Workflow Orchestration:** Uses Apache Airflow to coordinate tasks and monitor execution status.
- **Relational Data Storage:** Uses PostgreSQL to store structured datasets and processed sentiment results.
- **SQL Transformations:** Uses dbt models to organize staging data and build analytical marts.
- **Sentiment Analysis:** Processes customer reviews into positive, neutral, and negative sentiment categories.
- **Machine Learning:** Uses scikit-learn with TF-IDF and Logistic Regression for text classification and evaluation when suitable labeled data is available.
- **Interactive Dashboard:** Uses Streamlit and Plotly for data exploration, sentiment visualization, and model evaluation.
- **Data Quality Checks:** Examines missing values, duplicate records, and empty review text.
- **Containerization:** Uses Docker and Docker Compose to run application services locally.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Workflow Orchestration | Apache Airflow |
| Database | PostgreSQL |
| Data Transformation | dbt Core, dbt-postgres |
| Machine Learning | scikit-learn |
| Dashboard | Streamlit, Plotly |
| Query Language | SQL |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

## Project Structure

```text
AI-Data-Engineering-Pipeline/
├── ai/
│   ├── review_insights.py
│   └── sentiment_analysis.py
├── airflow/
│   ├── dags/
│   │   └── ai_data_pipeline.py
│   └── Dockerfile
├── dashboard/
│   └── app.py
├── dbt/
│   └── ai_data_pipeline/
│       ├── models/
│       │   ├── staging/
│       │   └── marts/
│       ├── dbt_project.yml
│       └── profiles.yml
├── ingestion/
│   └── generate_data.py
├── postgres/
│   └── init.sql
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Data Sources

The project uses locally generated synthetic datasets.

| Dataset | Previously generated rows | Description |
|---|---:|---|
| Customers | 1,000 | Customer information |
| Restaurants | 100 | Restaurant attributes |
| Food items | 300 | Menu item information |
| Orders | 10,000 | Order transactions |
| Order items | 24,812 | Items associated with orders |
| Reviews | 3,000 | Customer reviews and ratings |

These counts describe the previously generated datasets and may change when the data generator is rerun.

## Airflow Pipeline

The Airflow DAG is named `ai_data_engineering_pipeline`.

Its configured task sequence is:

1. **generate_data** — Generates the synthetic datasets.
2. **ai_sentiment_analysis** — Processes customer review sentiment.
3. **load_ai_results** — Loads sentiment results into PostgreSQL.
4. **dbt_build** — Executes dbt models and configured tests.

Task dependencies ensure that downstream tasks wait for their upstream tasks to complete successfully.

## PostgreSQL and dbt

PostgreSQL stores the structured datasets and analytical results. The project separates data into logical schemas:

- `raw` — Source datasets.
- `ai` — Processed sentiment results.
- `staging` — Intermediate transformation models.
- `marts` — Business-oriented analytical models.

The dbt project contains models for:

- `dim_customers` — Customer attributes.
- `dim_restaurants` — Restaurant attributes.
- `fct_orders` — Order-level data.
- `mart_daily_sales` — Daily sales and order metrics.
- `mart_restaurant_sentiment` — Restaurant-level sentiment insights.

The models support analysis of order activity, revenue, average order value, delivery metrics, restaurant performance, and review sentiment.

## Machine Learning and Sentiment Analysis

The project includes a local sentiment-processing workflow and an optional supervised machine learning workflow.

### Sentiment Processing

Customer reviews are processed into sentiment categories to help summarize customer feedback and compare restaurant-level sentiment.

### Scikit-learn Classification

The dashboard's machine learning section uses:

- **TF-IDF Vectorization:** Converts review text into numerical features.
- **Logistic Regression:** Predicts sentiment classes from the text features.
- **Train/Test Split:** Separates training examples from holdout evaluation examples.
- **Model Evaluation:** Displays accuracy, precision, recall, and F1-score through a classification report.

Supervised classification requires suitable labeled examples. Model performance depends on the quality of those labels and the representativeness of the test data.

## Interactive Dashboard

The Streamlit dashboard provides:

- Review data preview and filtering.
- Sentiment distribution visualization.
- Dataset quality checks.
- Machine learning model training and evaluation.
- Interactive sentiment prediction for entered review text.
- CSV export of filtered review data.

### Run the Dashboard

From the project root:

```powershell
python -m streamlit run dashboard/app.py
```

Open the local dashboard:

`http://localhost:8501`

## Run the Project Locally

### Prerequisites

- Python
- Git
- Docker Desktop
- Docker Compose

### 1. Clone the Repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/AI-Data-Engineering-Pipeline.git
cd AI-Data-Engineering-Pipeline
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start Docker Services

Start Docker Desktop, then run:

```powershell
docker compose up -d --build
```

### 5. Open Airflow

Navigate to:

`http://localhost:8080`

Open the `ai_data_engineering_pipeline` DAG to trigger and monitor the workflow.

### 6. Start the Dashboard

```powershell
python -m streamlit run dashboard/app.py
```

Navigate to:

`http://localhost:8501`

## Configuration and Security

- Keep local secrets in `.env` rather than committing them to GitHub.
- Use `.env.example` to document required environment variables without exposing actual credentials.
- Exclude virtual environments, logs, generated data, and temporary dbt artifacts when appropriate.
- Configure database credentials through environment variables for deployment.

## Future Improvements

- Automate ingestion of all raw datasets into PostgreSQL.
- Expand data quality checks and pipeline monitoring.
- Add persistent machine learning model storage.
- Improve sentiment classification with validated labeled data.
- Deploy the dashboard to a public hosting platform.
- Add a hosted database for accessible, persistent analytics.

## Project Status

The local dashboard is running, and the Airflow workflow has been executed. The final `dbt_build` task should be confirmed successful in Airflow before claiming that every stage has completed successfully for the latest run.

## Author

**Jaswanth Kumar Kommoju**

- **Email:** [jeswanthkumarkommuji@gmail.com](mailto:jeswanthkumarkommuji@gmail.com)
- **LinkedIn:** [jaswanthkumar06](https://www.linkedin.com/in/jaswanthkumar06)
- **GitHub:** [jaswanthkumar-06](https://github.com/jaswanthkumar-06)
- **Portfolio:** [View Portfolio](https://jaswanthkumar-06.github.io/my-portfolio/)

---

*Built to demonstrate data engineering workflows, SQL transformations, machine learning, and interactive analytics.*