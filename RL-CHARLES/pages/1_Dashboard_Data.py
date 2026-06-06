import streamlit as st
from src.app_utils import load_data, model_ready, rupiah
from src.ui_components import hero_section, section_header, metric_tile, status_badge, render_status_pills, get_plotly_theme

try:
    import plotly.express as px
except Exception:
    px = None

st.set_page_config(page_title="Dashboard Data", layout="wide")

ready = model_ready()
badge_class, badge_text = status_badge(ready, "Dataset & model ready", "Dataset atau model belum siap")
hero_section("Sales Analytics Overview", "Dashboard Data Penjualan", "", badge_class, badge_text)

if not ready:
    st.warning("Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu.")
    st.stop()

df = load_data()
daily_sales = df.groupby("tanggal", as_index=False)["total_penjualan"].sum()
category_sales = (
    df.groupby("kategori_produk", as_index=False)["total_penjualan"]
    .sum()
    .sort_values("total_penjualan", ascending=False)
)
promo_sales = df.groupby("promo_aktif", as_index=False)["total_penjualan"].mean()
promo_sales["status_promo"] = promo_sales["promo_aktif"].map({0: "Tanpa promo", 1: "Promo"})

# KPI Row
section_header("KPI Row", "Performance Summary", "")
kpi_cols = st.columns(4, gap="small")

with kpi_cols[0]:
    metric_tile("Total baris", f"{len(df):,}".replace(",", "."))
with kpi_cols[1]:
    metric_tile("Total penjualan", rupiah(df["total_penjualan"].sum()))
with kpi_cols[2]:
    metric_tile("Rata-rata transaksi", rupiah(df["total_penjualan"].mean()))
with kpi_cols[3]:
    metric_tile("Produk unik", str(df["id_produk"].nunique()))

# Main chart and snapshot
primary_col, side_col = st.columns([2.2, 1])

with primary_col:
    with st.container(border=True):
        section_header("Main Visual", "Daily Sales Trend", "")
        if px is not None:
            fig = px.line(
                daily_sales,
                x="tanggal",
                y="total_penjualan",
                markers=True,
                color_discrete_sequence=["#1E87EC"],
            )
            theme = get_plotly_theme()
            fig.update_layout(**theme["layout"])
            fig.update_traces(line=dict(width=3), marker=dict(size=7))
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(gridcolor="rgba(229,231,235,0.85)", tickprefix="Rp ")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.line_chart(daily_sales, x="tanggal", y="total_penjualan", height=390)

with side_col:
    with st.container(border=True):
        section_header("Snapshot", "Dataset Status", "")
        pills = [
            f"{df['kategori_produk'].nunique()} kategori",
            f"{df['kanal_penjualan'].nunique()} kanal",
            f"{daily_sales['tanggal'].nunique()} hari",
            f"Promo ratio {(df['promo_aktif'].mean() * 100):.1f}%",
        ]
        st.markdown(f"<div>{render_status_pills(pills)}</div>", unsafe_allow_html=True)

# Analysis panels
section_header("Breakdown Panels", "Category & Promo Impact", "")

panel_left, panel_right = st.columns(2)

with panel_left:
    with st.container(border=True):
        section_header("Category View", "Sales by Category", "")
        if px is not None:
            category_fig = px.bar(
                category_sales,
                x="kategori_produk",
                y="total_penjualan",
                color="kategori_produk",
                color_discrete_sequence=["#1E87EC", "#4DA3FF", "#74BAFF", "#AF1B09", "#F97316"],
            )
            theme = get_plotly_theme()
            fig_layout = {**theme["layout"], "height": 340, "showlegend": False}
            category_fig.update_layout(**fig_layout)
            category_fig.update_yaxes(gridcolor="rgba(229,231,235,0.85)", tickprefix="Rp ")
            st.plotly_chart(category_fig, use_container_width=True)
        else:
            st.bar_chart(category_sales, x="kategori_produk", y="total_penjualan", height=340)

with panel_right:
    with st.container(border=True):
        section_header("Promo View", "Average Sales by Promo", "")
        if px is not None:
            promo_fig = px.bar(
                promo_sales,
                x="status_promo",
                y="total_penjualan",
                color="status_promo",
                color_discrete_map={"Tanpa promo": "#CBD5E1", "Promo": "#AF1B09"},
                text_auto=".0f",
            )
            theme = get_plotly_theme()
            fig_layout = {**theme["layout"], "height": 340, "showlegend": False}
            promo_fig.update_layout(**fig_layout)
            promo_fig.update_yaxes(gridcolor="rgba(229,231,235,0.85)", tickprefix="Rp ")
            st.plotly_chart(promo_fig, use_container_width=True)
        else:
            st.bar_chart(promo_sales, x="status_promo", y="total_penjualan", height=340)

# Raw data preview
with st.container(border=True):
    section_header("Dataset Preview", "Raw Data Sample", "")
    st.dataframe(df.head(120), use_container_width=True)


