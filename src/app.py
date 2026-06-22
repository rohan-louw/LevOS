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

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

latest_date = df["date"].max()

recent_df = df[
    df["date"] >= latest_date - pd.Timedelta(days=90)
].copy()

st.title("LevOS")
st.subheader("Human Performance Operating System")


latest_score = round(
    df["readiness_score"].iloc[-1],
    1
)

latest = recent_df.iloc[-1]

avg_readiness = round(
    recent_df["readiness_score"].mean(),
    1
)

latest_score = round(latest["readiness_score"], 1)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Readiness", latest_score)

with col2:
    st.metric("HRV", round(latest["hrv_mean"], 1))

with col3:
    st.metric("Sleep", f"{round(latest['total_sleep'], 1)} h")

with col4:
    st.metric("90d Avg", avg_readiness)

chart_df = recent_df[["date", "readiness_score"]].copy()
chart_df = chart_df.set_index("date")

chart_df["readiness_7d"] = chart_df["readiness_score"].rolling(7).mean()

st.subheader("Readiness Trend — Last 90 Records")
st.line_chart(chart_df[["readiness_7d"]])

st.subheader("Recent Scores")

recent_table = recent_df[
    [
        "date",
        "readiness_score",
        "hrv_mean",
        "rhr_mean",
        "total_sleep",
        "sleep_deep"
    ]
].tail(10).copy()

recent_table["date"] = recent_table["date"].dt.date

st.dataframe(recent_table)