
import pandas as pd
import os

# STEP 1: Load the economic dataset

df = pd.read_csv("data/raw/economic_data.csv")

print("ECONOMIC DATA EXPLORATION")
print("=" * 50)

# STEP 2: Display first five records

print("\nFIRST FIVE RECORDS")
print(df.head())

# STEP 3: Check dataset dimensions

print("\nDATASET DIMENSIONS")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# STEP 4: Check column information

print("\nDATASET INFORMATION")
df.info()

# STEP 5: Check missing values

print("\nMISSING VALUES")
print(df.isnull().sum())

# STEP 6: Check duplicate records

print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# STEP 7: Generate descriptive statistics

print("\nDESCRIPTIVE STATISTICS")
print(df["Value"].describe())

# STEP 8: Calculate statistics by indicator

print("\nSTATISTICS BY ECONOMIC INDICATOR")

summary = df.groupby("Indicator")["Value"].agg(
    ["mean", "median", "min", "max", "std", "count"]
)

print(summary)

# STEP 9: Create processed data directory

os.makedirs("data/processed", exist_ok=True)
os.makedirs("outputs/results", exist_ok=True)

# STEP 10: Save summary statistics

summary.to_csv(
    "outputs/results/summary_statistics.csv"
)

print("\nAnalysis completed successfully!")
