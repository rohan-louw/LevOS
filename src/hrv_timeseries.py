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

output_path = project_root / "data" / "hrv_timeseries.csv"

target_type = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"

records = []

print("LevOS HRV Timeseries Extraction")
print("=" * 50)

for event, elem in ET.iterparse(xml_path, events=("end",)):
    if elem.tag == "Record" and elem.attrib.get("type") == target_type:
        records.append(
            {
                "start_date": elem.attrib.get("startDate"),
                "end_date": elem.attrib.get("endDate"),
                "value": float(elem.attrib.get("value")),
                "unit": elem.attrib.get("unit"),
                "source": elem.attrib.get("sourceName"),
            }
        )

    elem.clear()

df = pd.DataFrame(records)

df["start_date"] = pd.to_datetime(df["start_date"])
df["date"] = df["start_date"].dt.date

daily_hrv = (
    df.groupby("date")["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "hrv_mean"})
)

daily_hrv["hrv_7d_avg"] = daily_hrv["hrv_mean"].rolling(window=7).mean()
daily_hrv["hrv_30d_avg"] = daily_hrv["hrv_mean"].rolling(window=30).mean()

daily_hrv.to_csv(output_path, index=False)

print(f"Total HRV Records Extracted: {len(df)}")
print(f"Daily HRV Rows: {len(daily_hrv)}")
print(f"Saved to: {output_path}")

print("\nPreview:")
print(daily_hrv.head())