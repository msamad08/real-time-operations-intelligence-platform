from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "simulated"
DATA_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

n_zones = 100

zones = pd.DataFrame({
    "zone_id": [f"ZONE_{i:03d}" for i in range(1, n_zones + 1)],
    "latitude": np.random.uniform(35.8, 36.8, n_zones),
    "longitude": np.random.uniform(-87.5, -86.2, n_zones),
    "historical_job_volume": np.random.randint(10, 200, n_zones),
    "avg_response_time_minutes": np.random.randint(25, 180, n_zones),
    "estimated_revenue_exposure": np.random.randint(5000, 75000, n_zones)
})

weather = pd.DataFrame({
    "zone_id": zones["zone_id"],
    "rainfall_24hr": np.random.uniform(0, 8, n_zones),
    "wind_speed_max": np.random.uniform(5, 80, n_zones),
    "storm_severity_score": np.random.uniform(0, 1, n_zones)
})

iot = pd.DataFrame({
    "zone_id": zones["zone_id"],
    "moisture_sensor_avg": np.random.uniform(10, 100, n_zones),
    "humidity_sensor_avg": np.random.uniform(30, 100, n_zones),
    "sensor_alert_count": np.random.randint(0, 12, n_zones)
})

capacity = pd.DataFrame({
    "zone_id": zones["zone_id"],
    "crew_availability": np.random.randint(0, 10, n_zones),
    "equipment_units_available": np.random.randint(0, 8, n_zones),
    "current_workload": np.random.randint(0, 20, n_zones)
})

df = zones.merge(weather, on="zone_id") \
          .merge(iot, on="zone_id") \
          .merge(capacity, on="zone_id")

risk_score = (
    df["rainfall_24hr"] * 0.18 +
    df["wind_speed_max"] * 0.015 +
    df["storm_severity_score"] * 2.5 +
    df["moisture_sensor_avg"] * 0.025 +
    df["sensor_alert_count"] * 0.15 +
    df["historical_job_volume"] * 0.004 -
    df["crew_availability"] * 0.18 -
    df["equipment_units_available"] * 0.12
)

threshold = np.percentile(risk_score, 65)
df["high_demand_next_24hr"] = (risk_score >= threshold).astype(int)

df.to_csv(DATA_DIR / "operations_intelligence_data.csv", index=False)

print("Simulated operations intelligence dataset created.")
print(df.head())