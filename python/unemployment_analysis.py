
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# ECONOMIC INTELLIGENCE PROJECT
# UNEMPLOYMENT ANALYSIS
# ==========================================

# STEP 1: LOAD DATASET

file_path = "data/raw/economic_data.csv"

print("\n========== UNEMPLOYMENT ANALYSIS ==========")

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# STEP 2: FILTER UNEMPLOYMENT DATA

unemployment = df[
    df["Indicator"].astype("string").str.strip()
    == "Unemployment"
].copy()

# STEP 3: SELECT FIVE COUNTRIES

selected_codes = ["IND", "DEU", "USA", "CHN", "JPN"]

unemployment = unemployment[
    unemployment["Country_Code"].isin(selected_codes)
].copy()

# STEP 4: CLEAN DATA

unemployment["Year"] = pd.to_numeric(
    unemployment["Year"], errors="coerce"
)

unemployment["Value"] = pd.to_numeric(
    unemployment["Value"], errors="coerce"
)

unemployment = unemployment.dropna(
    subset=["Year", "Value"]
)

unemployment = unemployment.sort_values(
    ["Country", "Year"]
)

# STEP 5: DISPLAY RESULTS

print("\n========== UNEMPLOYMENT RESULTS ==========")

print("Total records:", len(unemployment))

print("\nCOUNTRY COVERAGE:")
print(unemployment.groupby("Country_Code").size())

print("\nFIRST 10 RECORDS:")
print(unemployment.head(10).to_string())

# STEP 6: CREATE CHART

if unemployment.empty:

    print("\nNo unemployment records found.")

else:

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 7))

    sns.lineplot(
        data=unemployment,
        x="Year",
        y="Value",
        hue="Country",
        marker="o"
    )

    plt.title(
        "Unemployment Comparison Across Countries",
        fontsize=16
    )

    plt.xlabel("Year")
    plt.ylabel("Unemployment Value (Dataset Units)")

    plt.legend(title="Country")
    plt.tight_layout()

    # STEP 7: SAVE CHART

    os.makedirs("outputs/charts", exist_ok=True)

    output_path = "outputs/charts/unemployment_comparison.png"

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nSUCCESS!")
    print("Unemployment chart created successfully!")
    print("Saved location:", output_path)

print("\n========== ANALYSIS COMPLETED ==========")
