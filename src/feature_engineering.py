from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "simulated" / "operations_intelligence_data.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_DATA)

# Operational capacity features
df["capacity_gap"] = df["current_workload"] - df["crew_availability"]
df["equipment_gap"] = df["current_workload"] - df["equipment_units_available"]

# Weather + sensor risk features
df["weather_risk_index"] = (
    df["rainfall_24hr"] * 0.4 +
    df["wind_speed_max"] * 0.03 +
    df["storm_severity_score"] * 4
)

df["sensor_risk_index"] = (
    df["moisture_sensor_avg"] * 0.04 +
    df["humidity_sensor_avg"] * 0.02 +
    df["sensor_alert_count"] * 0.5
)

# Operational pressure score
df["operational_pressure_score"] = (
    df["weather_risk_index"] +
    df["sensor_risk_index"] +
    df["capacity_gap"] * 0.3 +
    df["avg_response_time_minutes"] * 0.01
)

# Revenue exposure category
df["revenue_exposure_level"] = pd.cut(
    df["estimated_revenue_exposure"],
    bins=[0, 20000, 50000, 100000],
    labels=["Low", "Medium", "High"]
)

output_path = PROCESSED_DIR / "operations_features.csv"
df.to_csv(output_path, index=False)

print("Feature engineering complete.")
print(f"Saved processed data to: {output_path}")
print(df.head())