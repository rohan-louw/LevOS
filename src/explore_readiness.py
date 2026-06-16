from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_root / "data" / "readiness_dataset.csv"
)

print(df.info())
print()
print(df.describe())

print(df.head())