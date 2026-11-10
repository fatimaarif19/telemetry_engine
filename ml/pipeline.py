# ml/pipeline.py
import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_PATH = "models/isolation_forest.joblib"

def train_model():
    np.random.seed(42)
    cpu = np.random.uniform(10, 65, 1000)
    mem = np.random.uniform(20, 65, 1000)
    net = np.random.uniform(10, 100, 1000)
    req = np.random.uniform(100, 1000, 1000)
    X_normal = np.column_stack((cpu, mem, net, req))

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X_normal)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

class TelemetryDetector:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            train_model()
        self.model = joblib.load(MODEL_PATH)

    def predict(self, packet: dict) -> dict:
        features = np.array([[
            packet["cpu_usage"],
            packet["memory_usage"],
            packet["network_throughput_mbps"],
            packet["request_rate_rps"]
        ]])
        raw_pred = self.model.predict(features)[0]
        score = float(self.model.decision_function(features)[0])
        return {
            "is_anomaly": True if raw_pred == -1 else False,
            "anomaly_score": round(score, 4)
        }

if __name__ == "__main__":
    train_model()
    print("[+] ML Model trained and saved.")