from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "operations_features.csv"
ALERT_DIR = BASE_DIR / "outputs" / "reports"
ALERT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

alerts = []

for _, row in df.iterrows():
    if row["operational_pressure_score"] >= 18 and row["crew_availability"] < 3:
        alerts.append({
            "zone_id": row["zone_id"],
            "alert_level": "Critical",
            "operational_pressure_score": round(row["operational_pressure_score"], 2),
            "crew_availability": row["crew_availability"],
            "current_workload": row["current_workload"],
            "recommended_action": "Stage emergency crews and mitigation equipment immediately."
        })
    elif row["operational_pressure_score"] >= 12:
        alerts.append({
            "zone_id": row["zone_id"],
            "alert_level": "Moderate",
            "operational_pressure_score": round(row["operational_pressure_score"], 2),
            "crew_availability": row["crew_availability"],
            "current_workload": row["current_workload"],
            "recommended_action": "Monitor conditions and prepare staffing backup."
        })

alerts_df = pd.DataFrame(alerts)
alerts_df.to_csv(ALERT_DIR / "operational_alerts.csv", index=False)

print("Alerts generated successfully.")
print(alerts_df.head())