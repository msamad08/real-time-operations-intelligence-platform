import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "operations_features.csv"

# ==========================
# Cloud Deployment Data Check
# ==========================

import subprocess
import sys

if not DATA_PATH.exists():
    subprocess.run([sys.executable, str(BASE_DIR / "src" / "generate_data.py")], check=True)
    subprocess.run([sys.executable, str(BASE_DIR / "src" / "feature_engineering.py")], check=True)

df = pd.read_csv(DATA_PATH)

# ==========================
# Risk categories
# ==========================

df["risk_category"] = df["operational_pressure_score"].apply(
    lambda x: "Critical" if x >= 18
    else ("Moderate" if x >= 12 else "Low")
)

st.set_page_config(
    page_title="Operations Intelligence Dashboard",
    layout="wide"
)

st.title("Real-Time Operations Intelligence Dashboard")

st.markdown("""
Operational forecasting platform integrating:
- Weather risk
- IoT sensor activity
- Franchise capacity
- Operational pressure analytics
""")

# ==========================
# KPI Metrics
# ==========================

high_risk_count = df["high_demand_next_24hr"].sum()
avg_response = df["avg_response_time_minutes"].mean()
avg_pressure = df["operational_pressure_score"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("High Risk Zones", int(high_risk_count))
col2.metric("Avg Response Time", f"{avg_response:.1f} min")
col3.metric("Avg Operational Pressure", f"{avg_pressure:.2f}")

# ==========================
# Risk Map
# ==========================

st.subheader("Operational Risk Map")

fig_map = px.scatter_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    color="risk_category",
    color_discrete_map={
        "Critical": "red",
        "Moderate": "yellow",
        "Low": "green"
    },
    size="operational_pressure_score",
    hover_name="zone_id",
    hover_data=[
        "rainfall_24hr",
        "storm_severity_score",
        "crew_availability",
        "current_workload"
    ],
    zoom=6,
    height=600
)

fig_map.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig_map, use_container_width=True)

# ==========================
# Operational Pressure
# ==========================

st.subheader("Operational Pressure by Zone")

fig_pressure = px.bar(
    df.sort_values("operational_pressure_score", ascending=False).head(15),
    x="zone_id",
    y="operational_pressure_score",
    color="risk_category",
    color_discrete_map={
        "Critical": "red",
        "Moderate": "yellow",
        "Low": "green"
    }
)

st.plotly_chart(fig_pressure, use_container_width=True)

# ==========================
# Weather Risk
# ==========================

st.subheader("Weather Risk vs Sensor Risk")

fig_scatter = px.scatter(
    df,
    x="weather_risk_index",
    y="sensor_risk_index",
    color="risk_category",
    color_discrete_map={
        "Critical": "red",
        "Moderate": "yellow",
        "Low": "green"
    },
    size="historical_job_volume",
    hover_name="zone_id"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================
# Prediction Output / Recommendations
# ==========================

st.subheader("Prediction Output & Operational Recommendations")

top_risk = df.sort_values(
    "operational_pressure_score",
    ascending=False
).head(10)

recommendations = []

for _, row in top_risk.iterrows():
    if row["risk_category"] == "Critical":
        action = "Stage emergency response crews and mitigation equipment immediately."
    elif row["risk_category"] == "Moderate":
        action = "Monitor conditions and prepare additional staffing."
    else:
        action = "Maintain normal operational readiness."

    recommendations.append({
        "Zone": row["zone_id"],
        "Risk Category": row["risk_category"],
        "Operational Pressure": round(row["operational_pressure_score"], 2),
        "Crew Availability": row["crew_availability"],
        "Current Workload": row["current_workload"],
        "Recommended Action": action
    })

recommendation_df = pd.DataFrame(recommendations)

st.dataframe(recommendation_df, use_container_width=True)

# ==========================
# Operational Alerts
# ==========================

st.subheader("Operational Alerts")

alerts_path = BASE_DIR / "outputs" / "reports" / "operational_alerts.csv"

if alerts_path.exists():
    alerts_df = pd.read_csv(alerts_path)
    st.dataframe(alerts_df, use_container_width=True)
else:
    st.info("No alert file found. Run src/alerting.py to generate operational alerts.")

# ==========================
# Data Table
# ==========================

st.subheader("Operational Intelligence Data")

st.dataframe(df.head(25))