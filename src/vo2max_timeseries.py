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

output_path = project_root / "data" / "VO2Max_timeseries.csv"

target_type = "HKQuantityTypeIdentifierVO2Max"

records = []

print("LevOS VO2Max Timeseries Extraction")
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

daily_VO2Max = (
    df.groupby("date")["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "VO2Max_mean"})
)

daily_VO2Max["VO2Max_7d_avg"] = daily_VO2Max["VO2Max_mean"].rolling(window=7).mean()
daily_VO2Max["VO2Max_30d_avg"] = daily_VO2Max["VO2Max_mean"].rolling(window=30).mean()

daily_VO2Max.to_csv(output_path, index=False)

print(f"Total VO2Max Records Extracted: {len(df)}")
print(f"Daily VO2Max Rows: {len(daily_VO2Max)}")
print(f"Saved to: {output_path}")

print("\nPreview:")
print(daily_VO2Max.head())