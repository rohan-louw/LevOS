from pathlib import Path
import xml.etree.ElementTree as ET

print("LevOS XML Inventory")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent

xml_path = (
    project_root
    / "data"
    / "raw"
    / "apple_health_export"
    / "export.xml"
)

print(f"XML File: {xml_path}")

tree = ET.parse(xml_path)
root = tree.getroot()

from collections import Counter

record_types = Counter()

for child in root:
    if child.tag == "Record":
        record_type = child.attrib.get("type")
        record_types[record_type] += 1

print("\nTop Record Types:\n")

for record_type, count in record_types.most_common():
    print(f"{count:>10} | {record_type}")