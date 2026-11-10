
import requests

# Step 1: Store the World Bank API address
url = (
    "https://api.worldbank.org/v2/country/IND/"
    "indicator/NY.GDP.MKTP.KD.ZG"
    "?format=json&date=2020"
)

# Step 2: Send a request
response = requests.get(url, timeout=30)

# Step 3: Check the response
print("Status Code:", response.status_code)

# Step 4: Convert the response into JSON
data = response.json()

# Step 5: Extract India's GDP information
if len(data) > 1 and data[1]:

    record = data[1][0]

    print("\nINDIA GDP GROWTH")
    print("------------------------")
    print("Country:", record["country"]["value"])
    print("Year:", record["date"])
    print("GDP Growth:", record["value"], "%")

else:
    print("No data available")
