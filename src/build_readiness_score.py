from pathlib import Path
import pandas as pd

print("LevOS Readiness Score Builder")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

df = pd.read_csv(data_folder / "readiness_dataset.csv")

df = df.dropna(subset=[
    "hrv_mean",
    "hrv_30d_avg",
    "rhr_mean",
    "rhr_30d_avg",
    "sleep_in_bed",
    "sleep_deep"
])

df["hrv_score"] = (df["hrv_mean"] / df["hrv_30d_avg"]) * 100
df["rhr_score"] = (df["rhr_30d_avg"] / df["rhr_mean"]) * 100
df["total_sleep"] = (
    df["sleep_core"] +
    df["sleep_deep"] +
    df["sleep_rem"]
)

df["total_sleep"] = (
    df["sleep_core"] +
    df["sleep_deep"] +
    df["sleep_rem"]
)

df["sleep_score"] = (df["total_sleep"] / 8) * 100

df["deep_sleep_score"] = (df["sleep_deep"] / 1.0) * 100

df["readiness_score"] = (
    df["hrv_score"] * 0.40 +
    df["rhr_score"] * 0.30 +
    df["sleep_score"] * 0.20 +
    df["deep_sleep_score"] * 0.10
)

df["readiness_score"] = df["readiness_score"].clip(0, 100)

output_path = data_folder / "readiness_scores.csv"
df.to_csv(output_path, index=False)

print(f"Rows scored: {len(df)}")
print(f"Saved to: {output_path}")

print("\nLatest readiness scores:")
print(
    df[
        [
            "date",
            "hrv_mean",
            "rhr_mean",
            "total_sleep",
            "sleep_deep",
            "readiness_score"
        ]
    ].tail(10)
)