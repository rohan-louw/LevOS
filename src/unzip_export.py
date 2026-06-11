from pathlib import Path
import zipfile

project_root = Path(__file__).resolve().parent.parent

zip_path = project_root / "exports" / "LevOS.zip"
raw_data_folder = project_root / "data" / "raw"

raw_data_folder.mkdir(parents=True, exist_ok=True)

print("LevOS Export Extraction")
print("=" * 50)
print(f"ZIP File: {zip_path}")
print(f"Extracting to: {raw_data_folder}")

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(raw_data_folder)

print("✅ Extraction complete")