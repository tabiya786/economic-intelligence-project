
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# ECONOMIC INTELLIGENCE PROJECT
# FOREIGN DIRECT INVESTMENT ANALYSIS
# ==========================================


# STEP 1: LOAD DATASET

file_path = "data/raw/economic_data.csv"

print("\n========== FDI DATA ANALYSIS ==========")

if not os.path.exists(file_path):
    print("ERROR: Dataset file not found!")
    raise SystemExit

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# STEP 2: CHECK AVAILABLE INDICATORS

print("\nAVAILABLE INDICATORS:")
print(df["Indicator"].value_counts())


# STEP 3: FILTER FDI DATA

fdi = df[
    df["Indicator"].astype("string").str.strip() == "FDI"
].copy()


# STEP 4: SELECT FIVE COUNTRIES

selected_codes = ["IND", "DEU", "USA", "CHN", "JPN"]

fdi = fdi[
    fdi["Country_Code"].isin(selected_codes)
].copy()


# STEP 5: CLEAN DATA

fdi["Year"] = pd.to_numeric(
    fdi["Year"], errors="coerce"
)

fdi["Value"] = pd.to_numeric(
    fdi["Value"], errors="coerce"
)

fdi = fdi.dropna(
    subset=["Year", "Value"]
)

fdi = fdi.sort_values(
    ["Country", "Year"]
)


# STEP 6: CHECK RESULTS

print("\n========== FDI RESULTS ==========")

print("\nTotal FDI records:", len(fdi))

print("\nCOUNTRY COVERAGE:")
print(fdi.groupby("Country_Code").size())

print("\nCOUNTRIES FOUND:")
print(fdi["Country"].unique())

print("\nFIRST 10 FDI RECORDS:")
print(fdi.head(10).to_string())


# STEP 7: CREATE CHART

if fdi.empty:

    print("\nNo FDI records found.")
    print("Check the indicator name and country codes.")

else:

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 7))

    sns.lineplot(
        data=fdi,
        x="Year",
        y="Value",
        hue="Country",
        marker="o"
    )

    plt.title(
        "Foreign Direct Investment Comparison",
        fontsize=16
    )

    plt.xlabel("Year")
    plt.ylabel("FDI Value (Dataset Units)")

    plt.legend(title="Country")

    plt.tight_layout()


    # STEP 8: SAVE CHART

    os.makedirs(
        "outputs/charts",
        exist_ok=True
    )

    output_path = (
        "outputs/charts/fdi_comparison.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nSUCCESS!")
    print("FDI chart created successfully!")
    print("Saved location:", output_path)


print("\n========== FDI ANALYSIS COMPLETED ==========")
