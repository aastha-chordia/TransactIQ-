import json, os, joblib
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "ml_models" / "risk_model.joblib"
FEATURES = ["amount_eur", "is_new_beneficiary", "country_risk", "invoice_match",
            "corridor_failure_rate", "transaction_frequency"]

PROVIDERS = [
    {"name": "Provider Alpha", "fee": 8.5, "hours": 1.5, "reliability": 0.985},
    {"name": "Provider Beta", "fee": 5.0, "hours": 5.0, "reliability": 0.970},
    {"name": "Provider Gamma", "fee": 12.0, "hours": 0.8, "reliability": 0.992},
]

def train_if_missing():
    if MODEL_PATH.exists():
        return
    rng = np.random.default_rng(42)
    n = 3500
    X = np.column_stack([
        rng.lognormal(8.2, 1.0, n).clip(10, 2_000_000),
        rng.integers(0, 2, n),
        rng.beta(2, 5, n),
        rng.integers(0, 2, n),
        rng.beta(1.5, 15, n),
        rng.poisson(5, n).clip(0, 40),
    ])
    z = (-3.2 + 0.000006 * X[:,0] + 1.0*X[:,1] + 2.4*X[:,2]
         - 1.6*X[:,3] + 2.0*X[:,4] - 0.045*X[:,5])
    p = 1 / (1 + np.exp(-z))
    y = (rng.random(n) < p).astype(int)
    model = RandomForestClassifier(n_estimators=180, max_depth=10, min_samples_leaf=3,
                                   class_weight="balanced", random_state=42, n_jobs=-1)
    model.fit(X, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

def get_model():
    train_if_missing()
    return joblib.load(MODEL_PATH)

def predict_risk(payment):
    model = get_model()
    row = np.array([[payment["amount_eur"], payment["is_new_beneficiary"],
                     payment["country_risk"], payment["invoice_match"],
                     payment["corridor_failure_rate"], payment["transaction_frequency"]]])
    probability = float(model.predict_proba(row)[0][1])
    score = round(probability * 100, 1)
    level = "Low" if score < 30 else "Medium" if score < 60 else "High" if score < 85 else "Critical"
    contributions = explain(model, row[0])
    return score, level, contributions

def explain(model, row):
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        values = explainer.shap_values(row.reshape(1, -1))
        # Binary classifier output shape differs between SHAP versions.
        if isinstance(values, list):
            vals = np.asarray(values[-1]).reshape(-1)
        else:
            arr = np.asarray(values)
            vals = arr[0, :, 1] if arr.ndim == 3 else arr.reshape(-1)
        return [{"feature": name, "impact": round(float(value), 4)}
                for name, value in sorted(zip(FEATURES, vals), key=lambda x: abs(x[1]), reverse=True)]
    except Exception:
        importances = model.feature_importances_
        return [{"feature": name, "impact": round(float(value), 4)}
                for name, value in sorted(zip(FEATURES, importances), key=lambda x: x[1], reverse=True)]

def choose_route():
    # Lower is better: normalized cost + time, with a reliability penalty.
    scored = []
    for p in PROVIDERS:
        score = 0.35*(p["fee"]/12) + 0.35*(p["hours"]/5) + 0.30*(1-p["reliability"])*100
        scored.append((score, p["name"]))
    return min(scored)[1]

def policy_flags(payment):
    flags = []
    if payment["amount_eur"] > 25000:
        flags.append("High-value payment exceeds €25,000 review threshold")
    if not payment["invoice_match"]:
        flags.append("Invoice details do not match payment request")
    if payment["country"] in {"KP", "IR", "SY"}:
        flags.append("Destination is in the prototype restricted-country list")
    if payment["risk_score"] >= 85:
        flags.append("Critical ML risk score")
    return flags
