from pathlib import Path
import sqlite3
import pandas as pd

print("LevOS SQLite Loader")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"
db_path = data_folder / "levos.db"

csv_files = {
    "hrv": data_folder / "hrv_timeseries.csv",
    "sleep": data_folder / "sleep_timeseries.csv",
    "rhr": data_folder / "rhr_timeseries.csv",
    "respiratory_rate": data_folder / "respiratory_rate_timeseries.csv",
    "vo2max": data_folder / "vo2max_timeseries.csv",
}

conn = sqlite3.connect(db_path)

for table_name, csv_path in csv_files.items():
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {table_name}: {len(df)} rows")
    else:
        print(f"Missing file: {csv_path}")

conn.close()

print("=" * 50)
print(f"SQLite database created: {db_path}")