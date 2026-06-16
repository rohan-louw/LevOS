from pathlib import Path
import pandas as pd

print("LevOS Readiness Dataset Builder")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

hrv_path = data_folder / "hrv_timeseries.csv"
sleep_path = data_folder / "sleep_timeseries.csv"
rhr_path = data_folder / "rhr_timeseries.csv"
rr_path = data_folder / "respiratory_rate_timeseries.csv"
vo2_path = data_folder / "vo2max_timeseries.csv"

hrv = pd.read_csv(hrv_path)
sleep = pd.read_csv(sleep_path)
rhr = pd.read_csv(rhr_path)
rr = pd.read_csv(rr_path)
vo2 = pd.read_csv(vo2_path)

print("Files loaded successfully")

print(f"HRV rows: {len(hrv)}")
print(f"Sleep rows: {len(sleep)}")
print(f"RHR rows: {len(rhr)}")
print(f"Respiratory Rate rows: {len(rr)}")
print(f"VO2Max rows: {len(vo2)}")

readiness = (
    hrv
    .merge(rhr, on="date", how="outer")
    .merge(sleep, on="date", how="outer")
    .merge(rr, on="date", how="outer")

)

readiness = readiness.rename(columns={
    "HKCategoryValueSleepAnalysisAsleepCore": "sleep_core",
    "HKCategoryValueSleepAnalysisAsleepDeep": "sleep_deep",
    "HKCategoryValueSleepAnalysisAsleepREM": "sleep_rem",
    "HKCategoryValueSleepAnalysisAwake": "sleep_awake",
    "HKCategoryValueSleepAnalysisInBed": "sleep_in_bed",
    "HKCategoryValueSleepAnalysisAsleepUnspecified": "sleep_unspecified"
})

readiness = readiness.sort_values("date")

print("\nReadiness Dataset")
print("=" * 50)
print(f"Rows: {len(readiness)}")

print("\nColumns:")
print(readiness.columns)

print("\nFirst 5 rows:")
print(readiness.head())

print("\nMissing values:")
print("=" * 50)

print(readiness.isna().sum())

print("\nComplete records:")
print("=" * 50)

complete = readiness.dropna(
    subset=[
        "hrv_mean",
        "rhr_mean"
    ]
)

print("Rows with HRV + RHR:", len(complete))

readiness.to_csv(
    data_folder / "readiness_dataset.csv",
    index=False
)

print("\nSaved:")
print(data_folder / "readiness_dataset.csv")