from pathlib import Path
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "operations_features.csv"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "outputs" / "reports"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

target = "high_demand_next_24hr"

X = df.drop(columns=["zone_id", target], errors="ignore")
y = df[target]

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

new_model = RandomForestClassifier(
    n_estimators=250,
    random_state=42,
    class_weight="balanced"
)

new_model.fit(X_train, y_train)

new_probs = new_model.predict_proba(X_test)[:, 1]
new_auc = roc_auc_score(y_test, new_probs)

model_path = MODEL_DIR / "demand_forecast_model.pkl"
features_path = MODEL_DIR / "model_features.pkl"
performance_path = REPORT_DIR / "model_performance.txt"

old_auc = 0

if performance_path.exists():
    content = performance_path.read_text()
    for line in content.splitlines():
        if "ROC-AUC" in line:
            old_auc = float(line.split(":")[1].strip())

if new_auc >= old_auc:
    joblib.dump(new_model, model_path)
    joblib.dump(list(X.columns), features_path)

    performance_path.write_text(f"ROC-AUC: {new_auc:.4f}\nModel updated successfully.")
    print(f"Model updated. New ROC-AUC: {new_auc:.4f}")
else:
    print(f"Model not updated. Old ROC-AUC: {old_auc:.4f}, New ROC-AUC: {new_auc:.4f}")