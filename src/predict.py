from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "demand_forecast_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "model_features.pkl"

model = joblib.load(MODEL_PATH)
model_features = joblib.load(FEATURES_PATH)

def predict_demand(input_data: dict):
    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    for col in model_features:
        if col not in df.columns:
            df[col] = 0

    df = df[model_features]

    probability = model.predict_proba(df)[0][1]
    prediction = model.predict(df)[0]

    risk_level = "High" if prediction == 1 else "Low"

    return {
        "risk_level": risk_level,
        "demand_probability": round(float(probability), 4)
    }