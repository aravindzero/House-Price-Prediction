"""
Train and persist a simple regression model for house price prediction.

The script downloads the California Housing dataset, engineers a few features,
splits the data, trains a RandomForestRegressor, evaluates it, and saves the
model along with the feature list inside the ../model directory.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "model"
MODEL_PATH = MODEL_DIR / "model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"


def load_dataset() -> pd.DataFrame:
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame
    df["avg_rooms"] = df["AveRooms"]
    df["avg_bedrooms"] = df["AveBedrms"]
    df["house_age"] = df["HouseAge"]
    df["median_income"] = df["MedInc"]
    df["population"] = df["Population"]
    df["latitude"] = df["Latitude"]
    df["longitude"] = df["Longitude"]
    df["target"] = df["MedHouseVal"]
    columns = [
        "median_income",
        "avg_rooms",
        "avg_bedrooms",
        "population",
        "house_age",
        "latitude",
        "longitude",
    ]
    return df[columns + ["target"]]


def train() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    df = load_dataset()
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, preds))
    r2 = float(r2_score(y_test, preds))

    joblib.dump({"model": model, "features": list(X.columns)}, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps({"mae": mae, "r2": r2}, indent=2))
    print(f"Model saved to {MODEL_PATH}")
    print(f"MAE: {mae:.3f}, R^2: {r2:.3f}")


if __name__ == "__main__":
    train()

