from pathlib import Path
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "operations_features.csv"
MODEL_PATH = BASE_DIR / "models" / "demand_forecast_model.pkl"
FEATURES_PATH = BASE_DIR / "models" / "model_features.pkl"
OUTPUT_DIR = BASE_DIR / "outputs" / "figures"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

target = "high_demand_next_24hr"

X = df.drop(columns=["zone_id", target], errors="ignore")
X = pd.get_dummies(X, drop_first=True)

model_features = joblib.load(FEATURES_PATH)

for col in model_features:
    if col not in X.columns:
        X[col] = 0

X = X[model_features]

model = joblib.load(MODEL_PATH)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# For binary classification, use class 1 if SHAP returns list
if isinstance(shap_values, list):
    shap_values_to_plot = shap_values[1]
else:
    shap_values_to_plot = shap_values

shap.summary_plot(shap_values_to_plot, X, show=False)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "shap_summary.png", bbox_inches="tight")
plt.close()

print("SHAP explainability chart saved to outputs/figures/shap_summary.png")