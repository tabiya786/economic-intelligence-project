
import pandas as pd
import sqlite3
import os

# ==========================================
# ECONOMIC INTELLIGENCE PROJECT
# SQL DATABASE INTEGRATION
# ==========================================

print("\n========== SQL DATABASE INTEGRATION ==========")

# STEP 1: LOAD DATASET

file_path = "data/raw/economic_data.csv"

if not os.path.exists(file_path):
    print("ERROR: Dataset not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total records:", len(df))

# STEP 2: CLEAN DATA

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df = df.dropna(
    subset=["Country", "Country_Code", "Year", "Indicator", "Value"]
)

# STEP 3: CREATE DATABASE FOLDER

os.makedirs("data", exist_ok=True)

database_path = "data/economic_intelligence.db"

# STEP 4: CONNECT TO SQLITE DATABASE

connection = sqlite3.connect(database_path)

# STEP 5: STORE DATA IN DATABASE

df.to_sql(
    "economic_data",
    connection,
    if_exists="replace",
    index=False
)

print("\nData successfully stored in SQLite!")

# STEP 6: RUN SQL QUERIES

print("\n========== SQL QUERY 1 ==========")
print("Total records in database:")

query1 = """
SELECT COUNT(*) AS total_records
FROM economic_data;
"""

result1 = pd.read_sql_query(query1, connection)
print(result1.to_string(index=False))


print("\n========== SQL QUERY 2 ==========")
print("Number of records by indicator:")

query2 = """
SELECT Indicator, COUNT(*) AS total_records
FROM economic_data
GROUP BY Indicator
ORDER BY total_records DESC;
"""

result2 = pd.read_sql_query(query2, connection)
print(result2.to_string(index=False))


print("\n========== SQL QUERY 3 ==========")
print("Average value by country and indicator:")

query3 = """
SELECT
    Country,
    Indicator,
    ROUND(AVG(Value), 2) AS average_value
FROM economic_data
GROUP BY Country, Indicator
ORDER BY Country, Indicator;
"""

result3 = pd.read_sql_query(query3, connection)
print(result3.to_string(index=False))


print("\n========== SQL QUERY 4 ==========")
print("Latest available observation for each country and indicator:")

query4 = """
SELECT
    Country,
    Country_Code,
    Indicator,
    Year,
    Value
FROM economic_data AS e
WHERE Year = (
    SELECT MAX(e2.Year)
    FROM economic_data AS e2
    WHERE e2.Country_Code = e.Country_Code
      AND e2.Indicator = e.Indicator
)
ORDER BY Country, Indicator;
"""

result4 = pd.read_sql_query(query4, connection)
print(result4.to_string(index=False))

# STEP 7: CLOSE DATABASE CONNECTION

connection.close()

print("\nSUCCESS!")
print("SQLite database created successfully!")
print("Database location:", database_path)

print("\n========== SQL ANALYSIS COMPLETED ==========")
