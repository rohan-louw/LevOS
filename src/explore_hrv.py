import sqlite3
import pandas as pd

conn = sqlite3.connect("data/levos.db")

df = pd.read_sql(
    "SELECT * FROM hrv",
    conn
)

print("\nLEVOS HRV EXPLORATION")
print("=" * 40)

print("\nFirst 5 rows:")
print(df.head())

print("\nDate Range:")
print("First record:", df["date"].min())
print("Last record :", df["date"].max())
print("Total records:", len(df))

print("\nColumns:")
print(df.columns)

print("\nDataset info:")
print(df.info())

print("\nSummary statistics:")
print(df.describe())

conn.close()