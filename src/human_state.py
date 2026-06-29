from pathlib import Path
import pandas as pd

print("LevOS Human State Builder")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

df = pd.read_csv(data_folder / "readiness_scores.csv")

human_state = df[
    [
        "date",
        "readiness_score",
        "hrv_score",
        "sleep_score",
        "deep_sleep_score",
    ]
].copy()

human_state = human_state.rename(
    columns={
        "readiness_score": "recovery_score",
    }
)

human_state["human_state_score"] = (
    human_state["recovery_score"] * 0.40
    + human_state["hrv_score"] * 0.25
    + human_state["sleep_score"] * 0.25
    + human_state["deep_sleep_score"] * 0.10
)

human_state["human_state_score"] = human_state["human_state_score"].clip(0, 100)

output_path = data_folder / "human_state.csv"
human_state.to_csv(output_path, index=False)

print(f"Rows created: {len(human_state)}")
print(f"Saved to: {output_path}")

print("\nLatest human state:")
print(human_state.tail(10))