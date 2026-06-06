from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


DATA_PATH = Path("data/dummy_penjualan_umkm.csv")
MODEL_PATH = Path("models/random_forest_penjualan_umkm.joblib")
METRICS_PATH = Path("reports/model_metrics.json")
PREDICTIONS_PATH = Path("reports/prediksi_test.csv")
FEATURE_IMPORTANCE_PATH = Path("reports/feature_importance.csv")
TARGET = "total_penjualan"

NUMERIC_FEATURES = [
    "harga_satuan",
    "stok_awal",
    "diskon_persen",
    "promo_aktif",
    "akhir_pekan",
    "bulan",
    "musim_ramadan_lebaran",
    "jumlah_pengunjung",
    "rating_produk",
]

CATEGORICAL_FEATURES = [
    "nama_produk",
    "kategori_produk",
    "kanal_penjualan",
    "hari_dalam_minggu",
    "cuaca",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def load_dataset(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["tanggal"])
    df = df.sort_values(["tanggal", "id_produk"]).reset_index(drop=True)
    return df


def split_by_time(df: pd.DataFrame, test_ratio: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame]:
    unique_dates = np.array(sorted(df["tanggal"].unique()))
    split_index = int(len(unique_dates) * (1 - test_ratio))
    cutoff = unique_dates[split_index]
    train_df = df[df["tanggal"] < cutoff].copy()
    test_df = df[df["tanggal"] >= cutoff].copy()
    return train_df, test_df


def build_pipeline() -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )
    regressor = RandomForestRegressor(
        n_estimators=300,
        max_depth=18,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", regressor)])


def _rmse(y_true: pd.Series, y_pred: np.ndarray) -> float:
    return float(mean_squared_error(y_true, y_pred) ** 0.5)


def _mape(y_true: pd.Series, y_pred: np.ndarray) -> float:
    actual = np.asarray(y_true)
    prediction = np.asarray(y_pred)
    positive_mask = actual > 0
    if not positive_mask.any():
        return 0.0
    return float(np.mean(np.abs((actual[positive_mask] - prediction[positive_mask]) / actual[positive_mask])) * 100)


def evaluate(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": _rmse(y_true, y_pred),
        "r2": float(r2_score(y_true, y_pred)),
        "mape": _mape(y_true, y_pred),
    }


def feature_importance(pipeline: Pipeline) -> pd.DataFrame:
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]
    names = preprocessor.get_feature_names_out()
    cleaned_names = [name.replace("numeric__", "").replace("categorical__", "") for name in names]
    return (
        pd.DataFrame({"feature": cleaned_names, "importance": model.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )


def train() -> dict[str, object]:
    df = load_dataset(DATA_PATH)
    train_df, test_df = split_by_time(df)

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    pipeline = build_pipeline()
    cv = TimeSeriesSplit(n_splits=5)
    cv_scores = cross_val_score(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring="neg_mean_absolute_error",
        n_jobs=-1,
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    metrics = evaluate(y_test, predictions)
    metrics.update(
        {
            "cv_mae_mean": float(-cv_scores.mean()),
            "cv_mae_std": float(cv_scores.std()),
            "train_rows": int(len(train_df)),
            "test_rows": int(len(test_df)),
            "train_start": train_df["tanggal"].min().strftime("%Y-%m-%d"),
            "train_end": train_df["tanggal"].max().strftime("%Y-%m-%d"),
            "test_start": test_df["tanggal"].min().strftime("%Y-%m-%d"),
            "test_end": test_df["tanggal"].max().strftime("%Y-%m-%d"),
        }
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipeline,
            "features": FEATURES,
            "numeric_features": NUMERIC_FEATURES,
            "categorical_features": CATEGORICAL_FEATURES,
            "target": TARGET,
            "metrics": metrics,
        },
        MODEL_PATH,
    )

    output = test_df[["tanggal", "id_produk", "nama_produk", TARGET]].copy()
    output["prediksi_total_penjualan"] = predictions.round(0).astype(int)
    output["absolute_error"] = (output[TARGET] - output["prediksi_total_penjualan"]).abs()
    output.to_csv(PREDICTIONS_PATH, index=False)

    importance = feature_importance(pipeline)
    importance.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

    with METRICS_PATH.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    return {"metrics": metrics, "feature_importance": importance.head(15).to_dict("records")}


if __name__ == "__main__":
    result = train()
    print(json.dumps(result["metrics"], indent=2))
