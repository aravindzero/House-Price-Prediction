from __future__ import annotations

import logging
import json
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model"
MODEL_PATH = MODEL_DIR / "model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

app = Flask(__name__)
CORS(app)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Run backend/train_model.py to create it."
        )
    payload = joblib.load(MODEL_PATH)
    return payload["model"], payload["features"]


def load_metrics() -> Dict[str, float]:
    if not METRICS_PATH.exists():
        return {"mae": None, "r2": None}
    with METRICS_PATH.open() as fp:
        return json.load(fp)


MODEL, FEATURES = load_model()
METRICS = load_metrics()


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/model-info")
def model_info():
    return jsonify(
        {
            "features": FEATURES,
            "metrics": METRICS,
        }
    )


@app.post("/predict")
def predict():
    data: Dict[str, Any] = request.get_json(force=True)
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return (
            jsonify({"error": f"Missing features: {', '.join(missing)}"}),
            400,
        )

    try:
        values = np.array([[float(data[f]) for f in FEATURES]])
    except (TypeError, ValueError) as exc:
        logger.exception("Invalid input received")
        return jsonify({"error": f"Invalid numeric value: {exc}"}), 400

    try:
        prediction = MODEL.predict(values)[0]
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Prediction failed")
        return jsonify({"error": str(exc)}), 500

    return jsonify({"prediction": float(prediction), "currency": "100k USD"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

