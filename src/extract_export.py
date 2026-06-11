from pathlib import Path
import zipfile

project_root = Path(__file__).resolve().parent.parent

zip_path = project_root / "exports" / "LevOS.zip"

print(f"ZIP File: {zip_path}")

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    print("\nContents:")

    for file in zip_ref.namelist():
        if file.endswith(".xml"):
            print(file)