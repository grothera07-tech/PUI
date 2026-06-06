from __future__ import annotations

from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st

DATA_PATH = Path("data/dummy_penjualan_umkm.csv")
MODEL_PATH = Path("models/random_forest_penjualan_umkm.joblib")
METRICS_PATH = Path("reports/model_metrics.json")
PREDICTIONS_PATH = Path("reports/prediksi_test.csv")
FEATURE_IMPORTANCE_PATH = Path("reports/feature_importance.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["tanggal"])


@st.cache_resource
def load_model_bundle() -> dict[str, object]:
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_metrics() -> dict:
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_predictions() -> pd.DataFrame:
    return pd.read_csv(PREDICTIONS_PATH, parse_dates=["tanggal"])


@st.cache_data
def load_feature_importance() -> pd.DataFrame:
    return pd.read_csv(FEATURE_IMPORTANCE_PATH)


def is_ramadan_lebaran(date: pd.Timestamp) -> int:
    periods = [
        (pd.Timestamp("2024-03-12"), pd.Timestamp("2024-04-20")),
        (pd.Timestamp("2025-03-01"), pd.Timestamp("2025-04-10")),
    ]
    return int(any(start <= date <= end for start, end in periods))


def rupiah(value) -> str:
    return "Rp {:,.0f}".format(float(value)).replace(",", ".")


def model_ready() -> bool:
    return DATA_PATH.exists() and MODEL_PATH.exists() and METRICS_PATH.exists()


def predict_sales(input_row: dict[str, object]) -> float:
    bundle = load_model_bundle()
    pipeline = bundle["pipeline"]
    features = bundle["features"]
    X = pd.DataFrame([input_row])[features]
    return float(pipeline.predict(X)[0])