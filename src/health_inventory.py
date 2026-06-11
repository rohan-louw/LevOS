from pathlib import Path

print("=" * 50)
print("LevOS Health Data Inventory")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent

print(f"Project Root: {project_root}")

exports_folder = project_root / "exports"

print(f"Exports Folder: {exports_folder}")

if exports_folder.exists():
    print("✅ Exports folder found")
else:
    print("❌ Exports folder not found")

print("\nFiles in exports folder:")

for item in exports_folder.iterdir():
    print(f"- {item.name}")