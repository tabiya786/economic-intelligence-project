
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# ECONOMIC INTELLIGENCE PROJECT
# POPULATION GROWTH ANALYSIS
# ==========================================

# STEP 1: LOAD DATASET

file_path = "data/raw/economic_data.csv"

print("\n========== POPULATION GROWTH ANALYSIS ==========")

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# STEP 2: FILTER POPULATION GROWTH DATA

population = df[
    df["Indicator"].astype("string").str.strip()
    == "Population_Growth"
].copy()

# STEP 3: SELECT FIVE COUNTRIES

selected_codes = ["IND", "DEU", "USA", "CHN", "JPN"]

population = population[
    population["Country_Code"].isin(selected_codes)
].copy()

# STEP 4: CLEAN DATA

population["Year"] = pd.to_numeric(
    population["Year"], errors="coerce"
)

population["Value"] = pd.to_numeric(
    population["Value"], errors="coerce"
)

population = population.dropna(
    subset=["Year", "Value"]
)

population = population.sort_values(
    ["Country", "Year"]
)

# STEP 5: DISPLAY RESULTS

print("\n========== POPULATION RESULTS ==========")

print("Total records:", len(population))

print("\nCOUNTRY COVERAGE:")
print(population.groupby("Country_Code").size())

print("\nFIRST 10 RECORDS:")
print(population.head(10).to_string())

# STEP 6: CREATE VISUALISATION

if population.empty:

    print("\nNo population growth records found.")

else:

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 7))

    sns.lineplot(
        data=population,
        x="Year",
        y="Value",
        hue="Country",
        marker="o"
    )

    plt.title(
        "Population Growth Comparison",
        fontsize=16
    )

    plt.xlabel("Year")
    plt.ylabel("Population Growth (Dataset Units)")

    plt.legend(title="Country")

    plt.tight_layout()

    # STEP 7: SAVE CHART

    os.makedirs("outputs/charts", exist_ok=True)

    output_path = "outputs/charts/population_growth_comparison.png"

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nSUCCESS!")
    print("Population growth chart created successfully!")
    print("Saved location:", output_path)

print("\n========== ANALYSIS COMPLETED ==========")
