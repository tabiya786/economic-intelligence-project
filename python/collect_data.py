
import requests
import pandas as pd
import os

# 1. Define the countries
countries = [
    "IND", "DEU", "USA", "CHN", "JPN",
    "FRA", "GBR", "BRA", "ZAF", "IDN"
]

# 2. Define economic indicators
indicators = {
    "NY.GDP.MKTP.KD.ZG": "GDP_Growth",
    "FP.CPI.TOTL.ZG": "Inflation",
    "SL.UEM.TOTL.ZS": "Unemployment",
    "NY.GDP.PCAP.CD": "GDP_Per_Capita",
    "BX.KLT.DINV.CD.WD": "FDI",
    "SP.POP.GROW": "Population_Growth"
}

# 3. Create an empty list
all_data = []

print("ECONOMIC DATA COLLECTION")
print("=" * 40)

# 4. Collect data for each indicator
for code, name in indicators.items():

    print("\nDownloading:", name)

    url = (
        "https://api.worldbank.org/v2/country/"
        + ";".join(countries)
        + "/indicator/"
        + code
        + "?format=json&per_page=20000&date=2000:2023"
    )

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        result = response.json()

        if len(result) < 2 or result[1] is None:
            print("No data available:", name)
            continue

        # 5. Extract individual records
        for item in result[1]:

            all_data.append({
                "Country": item["country"]["value"],
                "Country_Code": item["countryiso3code"],
                "Year": int(item["date"]),
                "Indicator": name,
                "Value": item["value"]
            })

        print("Successfully downloaded:", name)

    except requests.exceptions.RequestException as error:
        print("Download failed:", error)

# 6. Convert the list into a DataFrame
df = pd.DataFrame(all_data)

# 7. Remove missing values
df = df.dropna(subset=["Value"])

# 8. Create the output folder
os.makedirs("data/raw", exist_ok=True)

# 9. Save the dataset
df.to_csv("data/raw/economic_data.csv", index=False)

# 10. Display the results
print("\n" + "=" * 40)
print("DATA COLLECTION COMPLETED")
print("=" * 40)

print("Total records:", len(df))
print("\nFirst five records:")
print(df.head())

print("\nCountries collected:")
print(df["Country"].nunique())

print("\nIndicators collected:")
print(df["Indicator"].nunique())
