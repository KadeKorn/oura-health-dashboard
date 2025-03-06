import os
import requests
import pandas as pd
from dotenv import load_dotenv

print("🚀 Running Oura Fetch Script...")

# Load environment variables
load_dotenv()
ACCESS_TOKEN = os.getenv("OURA_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("❌ ERROR: Missing Oura API Token! Check your .env file.")
    exit()

print("✅ API Token Loaded Successfully")

HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
endpoint = "https://api.ouraring.com/v2/usercollection/sleep"

# Set full date range
START_DATE = "2024-12-26"
END_DATE = "2025-03-05"
params = {"start_date": START_DATE, "end_date": END_DATE}

print(f"🔗 Sending API request to {endpoint} for {START_DATE} to {END_DATE}...")

# Make the API request
response = requests.get(endpoint, headers=HEADERS, params=params)

print(f"📝 Response Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    
    # 🔍 Debugging: Print the full response structure
    print("📊 Full API Response:")
    print(data)

    # 🔹 Try extracting sleep data from the correct key
    sleep_data = data.get("data", [])  # Use "data" instead of "sleep"

    if sleep_data:
        df = pd.DataFrame(sleep_data)
        
        # 🔹 Ensure that all available fields are included in the CSV
        df.to_csv("data/oura_sleep_full.csv", index=False)
        print("✅ All Sleep Data fetched and saved to data/oura_sleep_full.csv!")
    else:
        print("⚠️ No sleep data found for the given date range.")
else:
    print(f"❌ API Request Failed! Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
