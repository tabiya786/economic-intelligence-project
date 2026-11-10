
import pandas as pd
import os

# ==========================================
# ECONOMIC INTELLIGENCE PROJECT
# CROSS-COUNTRY ECONOMIC ANALYSIS
# ==========================================

print("\n========== CROSS-COUNTRY ANALYSIS ==========")

# STEP 1: LOAD DATA

file_path = "data/raw/economic_data.csv"

if not os.path.exists(file_path):
    print("ERROR: Dataset not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Original dataset shape:", df.shape)

# STEP 2: SELECT COUNTRIES

selected_codes = ["IND", "DEU", "USA", "CHN", "JPN"]

df = df[df["Country_Code"].isin(selected_codes)].copy()

# STEP 3: CLEAN DATA

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df = df.dropna(subset=["Year", "Value"])

# STEP 4: SELECT LATEST AVAILABLE YEAR
# FOR EACH COUNTRY AND INDICATOR

df = df.sort_values("Year")

latest = df.loc[
    df.groupby(["Country_Code", "Indicator"])["Year"].idxmax()
].copy()

# STEP 5: CREATE COMPARISON TABLE

comparison = latest.pivot(
    index=["Country", "Country_Code"],
    columns="Indicator",
    values="Value"
)

comparison_years = latest.pivot(
    index=["Country", "Country_Code"],
    columns="Indicator",
    values="Year"
)

comparison.columns.name = None
comparison_years.columns = [
    str(col) + "_Year" for col in comparison_years.columns
]
comparison_years.columns.name = None

final_table = pd.concat(
    [comparison, comparison_years],
    axis=1
).reset_index()

# STEP 6: DISPLAY RESULTS

print("\n========== ECONOMIC COMPARISON ==========")

print(final_table.to_string(index=False))

print("\nCOUNTRIES INCLUDED:")
print(final_table["Country"].tolist())

print("\nINDICATORS INCLUDED:")
print(comparison.columns.tolist())

# STEP 7: SAVE RESULTS

os.makedirs("outputs/reports", exist_ok=True)

output_path = "outputs/reports/country_economic_comparison.csv"

final_table.to_csv(output_path, index=False)

print("\nSUCCESS!")
print("Cross-country comparison completed!")
print("Report saved at:", output_path)

print("\n========== ANALYSIS COMPLETED ==========")
