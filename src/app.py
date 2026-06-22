import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="LevOS",
    page_icon="📈",
    layout="wide"
)

project_root = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    project_root / "data" / "readiness_scores.csv"
)

st.title("LevOS")
st.subheader("Human Performance Operating System")

latest_score = round(
    df["readiness_score"].iloc[-1],
    1
)

st.metric(
    label="Today's Readiness",
    value=latest_score
)

chart_df = df[["date", "readiness_score"]].copy()
chart_df["date"] = pd.to_datetime(chart_df["date"])
chart_df = chart_df.set_index("date")



chart_df["readiness_7d"] = (
    chart_df["readiness_score"]
    .rolling(7)
    .mean()
)

st.line_chart(chart_df[["readiness_7d"]])

st.subheader("Recent Scores")

st.dataframe(
    df[
        [
            "date",
            "readiness_score",
            "hrv_mean",
            "rhr_mean",
            "total_sleep",
            "sleep_deep"
        ]
    ].tail(10)
)