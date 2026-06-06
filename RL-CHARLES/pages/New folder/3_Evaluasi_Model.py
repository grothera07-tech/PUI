import streamlit as st

from src.app_utils import load_feature_importance, load_metrics, load_predictions, model_ready, rupiah


st.title("Evaluasi Model Random Forest")

if not model_ready():
    st.warning("Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu.")
    st.stop()

metrics = load_metrics()
predictions = load_predictions()
importance = load_feature_importance()

metric_a, metric_b, metric_c, metric_d = st.columns(4)
metric_a.metric("MAE", rupiah(metrics["mae"]))
metric_b.metric("RMSE", rupiah(metrics["rmse"]))
metric_c.metric("R2", f"{metrics['r2']:.3f}")
metric_d.metric("MAPE", f"{metrics['mape']:.2f}%")

st.subheader("Aktual vs prediksi pada data uji")
plot_df = predictions.groupby("tanggal", as_index=False)[["total_penjualan", "prediksi_total_penjualan"]].sum()
st.line_chart(plot_df, x="tanggal", y=["total_penjualan", "prediksi_total_penjualan"], height=320)

left, right = st.columns(2)
with left:
    st.subheader("Feature importance")
    st.bar_chart(importance.head(15), x="feature", y="importance", height=340)

with right:
    st.subheader("Error terbesar")
    st.dataframe(predictions.sort_values("absolute_error", ascending=False).head(20), use_container_width=True)

st.subheader("Ringkasan split data")
st.dataframe(
    {
        "train_start": [metrics["train_start"]],
        "train_end": [metrics["train_end"]],
        "test_start": [metrics["test_start"]],
        "test_end": [metrics["test_end"]],
        "train_rows": [metrics["train_rows"]],
        "test_rows": [metrics["test_rows"]],
        "cv_mae_mean": [metrics["cv_mae_mean"]],
        "cv_mae_std": [metrics["cv_mae_std"]],
    },
    use_container_width=True,
)
