import sqlite3

conn = sqlite3.connect("data/levos.db")

cursor = conn.cursor()

tables = [
    "hrv",
    "sleep",
    "rhr",
    "respiratory_rate",
    "vo2max"
]

print("\nLEVOS DATABASE CHECK")
print("=" * 40)

for table in tables:
    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count} rows")

conn.close()