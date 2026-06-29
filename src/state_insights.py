from pathlib import Path
import pandas as pd

print("LevOS State Insights Builder")
print("=" * 50)

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / "data"

df = pd.read_csv(data_folder / "human_state.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

def classify_state(score):
    if score >= 90:
        return "Excellent"
    elif score >= 80:
        return "Good"
    elif score >= 70:
        return "Moderate"
    else:
        return "Poor"

def classify_trend(delta):
    if delta > 2:
        return "Improving"
    elif delta < -2:
        return "Declining"
    else:
        return "Stable"

def build_insight(state, trend):
    if state == "Excellent" and trend == "Improving":
        return "Human state is excellent and improving."
    elif state == "Excellent" and trend == "Stable":
        return "Human state remains excellent."
    elif state == "Excellent" and trend == "Declining":
        return "Human state is excellent but starting to decline."
    elif state == "Good" and trend == "Improving":
        return "Human state is good and improving."
    elif state == "Good" and trend == "Stable":
        return "Human state is stable and good."
    elif state == "Good" and trend == "Declining":
        return "Human state is good but trending downward."
    elif state == "Moderate" and trend == "Improving":
        return "Human state is recovering from a moderate level."
    elif state == "Moderate" and trend == "Stable":
        return "Human state is moderate and stable."
    elif state == "Moderate" and trend == "Declining":
        return "Human state is moderate and declining."
    elif state == "Poor" and trend == "Improving":
        return "Human state is poor but improving."
    elif state == "Poor" and trend == "Stable":
        return "Human state remains poor."
    else:
        return "Human state is poor and declining."

df["previous_score"] = df["human_state_score"].shift(1)
df["state_delta"] = df["human_state_score"] - df["previous_score"]

df["state"] = df["human_state_score"].apply(classify_state)
df["trend"] = df["state_delta"].fillna(0).apply(classify_trend)

df["insight"] = df.apply(
    lambda row: build_insight(row["state"], row["trend"]),
    axis=1
)

state_insights = df[
    [
        "date",
        "human_state_score",
        "previous_score",
        "state_delta",
        "state",
        "trend",
        "insight",
    ]
].copy()

output_path = data_folder / "state_insights.csv"
state_insights.to_csv(output_path, index=False)

print(f"Rows created: {len(state_insights)}")
print(f"Saved to: {output_path}")

print("\nLatest state insights:")
print(state_insights.tail(10))