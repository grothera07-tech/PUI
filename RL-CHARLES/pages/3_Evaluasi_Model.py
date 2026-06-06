import pandas as pd
import streamlit as st
from src.app_utils import (
    load_feature_importance,
    load_metrics,
    load_predictions,
    model_ready,
    rupiah,
)
from src.ui_components import hero_section, section_header, metric_tile, status_badge, render_status_pills, get_plotly_theme

try:
    import plotly.express as px
except Exception:
    px = None

st.set_page_config(page_title="Evaluasi Model", layout="wide")

ready = model_ready()
badge_class, badge_text = status_badge(ready, "Evaluation assets ready", "Artefak evaluasi belum siap")
hero_section("Model Performance Review", "Evaluasi Model Random Forest", "", badge_class, badge_text)

if not ready:
    st.warning(
        "Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu."
    )
    st.stop()

metrics = load_metrics()
predictions = load_predictions()
importance = load_feature_importance()

# KPI Metrics
section_header("Performance KPI", "Evaluation Metrics", "")
metric_cols = st.columns(4)

with metric_cols[0]:
    metric_tile("MAE", rupiah(metrics["mae"]))
with metric_cols[1]:
    metric_tile("RMSE", rupiah(metrics["rmse"]))
with metric_cols[2]:
    metric_tile("R2", f"{float(metrics['r2']):.3f}")
with metric_cols[3]:
    metric_tile("MAPE", f"{float(metrics['mape']):.2f}%")

# Main chart and snapshot
main_col, side_col = st.columns([2.1, 1], gap="large")

plot_df = predictions.groupby("tanggal", as_index=False)[
    ["total_penjualan", "prediksi_total_penjualan"]
].sum()

with main_col:
    with st.container(border=True):
        section_header("Main Analysis", "Actual vs Prediction", "")

        if px is not None:
            plot_long = plot_df.melt(
                id_vars="tanggal",
                value_vars=["total_penjualan", "prediksi_total_penjualan"],
                var_name="seri",
                value_name="nilai",
            )

            fig = px.line(
                plot_long,
                x="tanggal",
                y="nilai",
                color="seri",
                markers=True,
                color_discrete_map={
                    "total_penjualan": "#1E87EC",
                    "prediksi_total_penjualan": "#AF1B09",
                },
            )

            theme = get_plotly_theme()
            fig.update_layout(**theme["layout"])
            fig.update_traces(line=dict(width=3), marker=dict(size=7))
            fig.update_yaxes(gridcolor="rgba(229,231,235,0.85)", tickprefix="Rp ")
            fig.for_each_trace(
                lambda t: t.update(
                    name="Aktual" if t.name == "total_penjualan" else "Prediksi"
                )
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(
                plot_df,
                x="tanggal",
                y=["total_penjualan", "prediksi_total_penjualan"],
                height=390,
            )

with side_col:
    with st.container(border=True):
        section_header("Evaluation Snapshot", "Model Quick View", "")

        pills = [
            f"Train rows {metrics['train_rows']}",
            f"Test rows {metrics['test_rows']}",
            f"CV MAE {float(metrics['cv_mae_mean']):.2f}",
            f"CV std {float(metrics['cv_mae_std']):.2f}",
        ]
        st.markdown(f"<div>{render_status_pills(pills)}</div>", unsafe_allow_html=True)

# Analysis panels
section_header("Insight Panels", "Feature & Error Analysis", "")

left_panel, right_panel = st.columns(2, gap="large")

with left_panel:
    with st.container(border=True):
        section_header("Feature Drivers", "Feature Importance", "")

        top_importance = importance.head(15)

        if px is not None:
            importance_fig = px.bar(
                top_importance,
                x="importance",
                y="feature",
                orientation="h",
                color="importance",
                color_continuous_scale=[[0, "#dbeafe"], [1, "#1E87EC"]],
            )

            theme = get_plotly_theme()
            fig_layout = {**theme["layout"], "height": 430, "coloraxis_showscale": False}
            importance_fig.update_layout(**fig_layout)
            importance_fig.update_xaxes(gridcolor="rgba(229,231,235,0.85)")
            importance_fig.update_yaxes(categoryorder="total ascending")

            st.plotly_chart(importance_fig, use_container_width=True)
        else:
            st.bar_chart(top_importance, x="feature", y="importance", height=390)

with right_panel:
    with st.container(border=True):
        section_header("Error Review", "Top 20 Errors", "")

        error_df = predictions.sort_values("absolute_error", ascending=False).head(20).copy()

        if "absolute_error" in error_df.columns:
            styled_error_df = error_df.style.background_gradient(
                subset=["absolute_error"], cmap="OrRd"
            )
            st.dataframe(styled_error_df, use_container_width=True)
        else:
            st.dataframe(error_df, use_container_width=True)

# Split summary
with st.container(border=True):
    section_header("Split Summary", "Train-Test Split", "")

    split_df = pd.DataFrame(
        {
            "train_start": [metrics["train_start"]],
            "train_end": [metrics["train_end"]],
            "test_start": [metrics["test_start"]],
            "test_end": [metrics["test_end"]],
            "train_rows": [metrics["train_rows"]],
            "test_rows": [metrics["test_rows"]],
            "cv_mae_mean": [metrics["cv_mae_mean"]],
            "cv_mae_std": [metrics["cv_mae_std"]],
        }
    )

    st.dataframe(split_df, use_container_width=True, hide_index=True)


