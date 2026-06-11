from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

xml_path = (
    project_root
    / "data"
    / "raw"
    / "apple_health_export"
    / "export.xml"
)

output_path = project_root / "data" / "sleep_timeseries.csv"

target_type = "HKCategoryTypeIdentifierSleepAnalysis"

records = []

print("LevOS Sleep Timeseries Extraction")
print("=" * 50)

for event, elem in ET.iterparse(xml_path, events=("end",)):
    if elem.tag == "Record" and elem.attrib.get("type") == target_type:
        records.append(
            {
                "start_date": elem.attrib.get("startDate"),
                "end_date": elem.attrib.get("endDate"),
                "value": elem.attrib.get("value"),
                "source": elem.attrib.get("sourceName"),
            }
        )

    elem.clear()

df = pd.DataFrame(records)

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

df["duration_hours"] = (
    df["end_date"] - df["start_date"]
).dt.total_seconds() / 3600

df["date"] = df["start_date"].dt.date

daily_sleep = (
    df.groupby(["date", "value"])["duration_hours"]
    .sum()
    .reset_index()
)

sleep_pivot = daily_sleep.pivot(
    index="date",
    columns="value",
    values="duration_hours"
).fillna(0)

sleep_pivot = sleep_pivot.reset_index()

sleep_pivot.to_csv(output_path, index=False)

print(f"Total Sleep Records Extracted: {len(df)}")
print(f"Daily Sleep Rows: {len(sleep_pivot)}")
print(f"Saved to: {output_path}")

print("\nSleep Categories:")
print(df["value"].value_counts())

print("\nPreview:")
print(sleep_pivot.head())