from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_root / "data" / "readiness_dataset.csv"
)

print(df.info())
print()
print(df.describe())

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df.head())

print("\nLatest 5 rows:")
print(
    df[
        [
            "date",
            "sleep_core",
            "sleep_deep",
            "sleep_rem",
            "sleep_awake",
            "sleep_in_bed"
        ]
    ].tail(20)
)

df["total_sleep"] = (
    df["sleep_core"] +
    df["sleep_deep"] +
    df["sleep_rem"]
)

print(
    df[
        [
            "date",
            "total_sleep",
            "sleep_deep"
        ]
    ].tail(10)
)