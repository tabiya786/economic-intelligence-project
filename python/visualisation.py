
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================
# ECONOMIC INTELLIGENCE PROJECT
# GDP PER CAPITA COUNTRY COMPARISON
# ============================================


# STEP 1: LOAD DATASET

file_path = "data/raw/economic_data.csv"

print("\n========== DATASET LOADING ==========")

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())


# STEP 2: INSPECT DATASET

print("\n========== DATASET INSPECTION ==========")

print("\nFirst 10 records:")
print(df.head(10).to_string())

print("\nAvailable indicators:")
print(df["Indicator"].value_counts().to_string())

print("\nAvailable countries:")
print(df["Country"].unique())


# STEP 3: FILTER GDP PER CAPITA DATA

print("\n========== GDP PER CAPITA ANALYSIS ==========")

# IMPORTANT:
# Our dataset contains GDP_Per_Capita,
# NOT GDP_Growth.

gdp = df[
    df["Indicator"].astype("string").str.strip()
    == "GDP_Per_Capita"
].copy()


# STEP 4: SELECT FIVE COUNTRIES

selected_codes = ["IND", "DEU", "USA", "CHN", "JPN"]

gdp = gdp[
    gdp["Country_Code"].isin(selected_codes)
].copy()


# STEP 5: CLEAN DATA

gdp["Year"] = pd.to_numeric(
    gdp["Year"],
    errors="coerce"
)

gdp["Value"] = pd.to_numeric(
    gdp["Value"],
    errors="coerce"
)

gdp = gdp.dropna(
    subset=["Year", "Value"]
)

gdp = gdp.sort_values(
    ["Country", "Year"]
)


# STEP 6: VALIDATE RESULTS

print("\nTotal GDP PER CAPITA records:")
print(len(gdp))

print("\nCOUNTRY COVERAGE:")
print(gdp.groupby("Country_Code").size())

print("\nCOUNTRIES FOUND:")
print(gdp["Country"].unique())

print("\nFIRST 10 GDP RECORDS:")
print(gdp.head(10).to_string())


# STEP 7: CREATE VISUALISATION

if gdp.empty:

    print("\nNo GDP per capita records found.")
    print("Please check the dataset and country codes.")

else:

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 7))

    sns.lineplot(
        data=gdp,
        x="Year",
        y="Value",
        hue="Country",
        marker="o"
    )

    plt.title(
        "GDP Per Capita Comparison: Five Countries",
        fontsize=16
    )

    plt.xlabel("Year")
    plt.ylabel("GDP Per Capita")

    plt.legend(
        title="Country",
        loc="best"
    )

    plt.tight_layout()


    # STEP 8: SAVE CHART

    os.makedirs(
        "outputs/charts",
        exist_ok=True
    )

    output_path = (
        "outputs/charts/gdp_per_capita_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nSUCCESS!")
    print("Chart created successfully.")

    print("Saved location:", output_path)


print("\n========== PROJECT EXECUTION COMPLETED ==========")
