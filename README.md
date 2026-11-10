
# Economic Intelligence Project

## Overview

The Economic Intelligence Project is a Python-based data analytics project that explores key economic indicators across selected countries using World Bank data.

The project demonstrates data collection through an API, data cleaning, exploratory analysis, SQL queries, data visualization, and an interactive dashboard.

## Objectives

- Collect economic data using the World Bank API.
- Analyze economic indicators across multiple countries.
- Compare country-level economic trends.
- Use SQL to query and summarize economic data.
- Build an interactive dashboard using Streamlit.

## Countries Covered

India, Germany, United States, China, Japan, France, United Kingdom, Brazil, South Africa, and Indonesia.

## Economic Indicators

- GDP per Capita
- Foreign Direct Investment (FDI)
- Population Growth
- Unemployment

## Tools and Technologies

- Python
- Pandas
- Requests
- Matplotlib
- Seaborn
- Plotly
- SQL
- SQLite
- Streamlit
- Git and GitHub

## Project Structure

```text
Economic-Intelligence-Project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── raw/
│       └── economic_data.csv
│
├── outputs/
│   ├── charts/
│   └── reports/
│
└── python/
    ├── collect_data.py
    ├── explore_data.py
    ├── visualisation.py
    ├── fdi_analysis.py
    ├── population_analysis.py
    ├── unemployment_analysis.py
    ├── cross_country_analysis.py
    └── sql_analysis.py
```

## Data Source

Data is collected from the World Bank Open Data API.

API: https://api.worldbank.org/

The collection script requests selected economic indicators for the period 2000–2023. The available records in the processed dataset depend on data availability.

## Key Features

1. API-based economic data collection.
2. Data exploration and cleaning using Pandas.
3. Country-level economic indicator comparisons.
4. Economic data visualization.
5. SQL-based analysis using SQLite.
6. Interactive Streamlit dashboard.

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd Economic-Intelligence-Project
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

## Project Status

Completed initial data collection, analysis scripts, visualizations, SQL analysis, and dashboard development.

Further improvements may include additional indicators, historical trend analysis, and dashboard enhancements.

## Author

Data Analytics Portfolio Project
