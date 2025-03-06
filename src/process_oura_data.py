import pandas as pd

print("🚀 Processing Oura Sleep Data...")

# Load raw data
try:
    df = pd.read_csv("data/oura_sleep_full.csv")
    print("✅ Raw Data Loaded Successfully!")
except FileNotFoundError:
    print("❌ ERROR: Oura sleep data file not found! Run 'oura_fetch.py' first.")
    exit()

# ✅ Print available columns to confirm structure
print("📝 Available Columns in Data:")
print(df.columns)

# ✅ Rename the correct date column
if "day" in df.columns:
    df.rename(columns={"day": "summary_date"}, inplace=True)
    print("✅ Renamed 'day' to 'summary_date'")
elif "bedtime_start" in df.columns:
    df.rename(columns={"bedtime_start": "summary_date"}, inplace=True)
    print("✅ Renamed 'bedtime_start' to 'summary_date'")
else:
    print("❌ ERROR: No valid date column found! Stopping script.")
    exit()

# Convert summary_date to datetime format
df["summary_date"] = pd.to_datetime(df["summary_date"])

# Select important columns
columns_of_interest = [
    "summary_date",
    "total_sleep_duration",
    "rem_sleep_duration",
    "deep_sleep_duration",
    "restless_periods",
    "sleep_score_delta",
    "time_in_bed"
]

# ✅ Keep only the selected columns
df_cleaned = df[columns_of_interest].copy()

# Convert sleep duration from seconds to hours
df_cleaned["total_sleep_hours"] = df_cleaned["total_sleep_duration"] / 3600
df_cleaned["rem_sleep_hours"] = df_cleaned["rem_sleep_duration"] / 3600
df_cleaned["deep_sleep_hours"] = df_cleaned["deep_sleep_duration"] / 3600

# Save cleaned data
df_cleaned.to_csv("data/oura_sleep_cleaned.csv", index=False)
print("✅ Processed Data Saved to 'data/oura_sleep_cleaned.csv'")
