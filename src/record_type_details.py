from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

project_root = Path(__file__).resolve().parent.parent

xml_path = (
    project_root
    / "data"
    / "raw"
    / "apple_health_export"
    / "export.xml"
)

target_type = "HKQuantityTypeIdentifierHeartRateVariabilitySDNN"

values = []
dates = []

print("LevOS Record Type Details")
print("=" * 50)
print(f"Target Type: {target_type}")
print(f"XML File: {xml_path}")

for event, elem in ET.iterparse(xml_path, events=("end",)):
    if elem.tag == "Record" and elem.attrib.get("type") == target_type:
        value = float(elem.attrib.get("value"))
        start_date = elem.attrib.get("startDate")

        values.append(value)
        dates.append(start_date)

    elem.clear()

print("\nSummary")
print("=" * 50)
print(f"Total Records: {len(values)}")

if values:
    print(f"Min Value: {min(values):.2f}")
    print(f"Max Value: {max(values):.2f}")
    print(f"Average Value: {sum(values) / len(values):.2f}")

    print(f"Earliest Date: {min(dates)}")
    print(f"Latest Date: {max(dates)}")