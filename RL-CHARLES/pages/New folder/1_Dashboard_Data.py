import streamlit as st

from src.app_utils import model_ready, rupiah, load_data


st.title("Dashboard Data Penjualan UMKM")

if not model_ready():
    st.warning("Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu.")
    st.stop()

df = load_data()
daily_sales = df.groupby("tanggal", as_index=False)["total_penjualan"].sum()
category_sales = df.groupby("kategori_produk", as_index=False)["total_penjualan"].sum().sort_values("total_penjualan", ascending=False)
promo_sales = df.groupby("promo_aktif", as_index=False)["total_penjualan"].mean()

metric_a, metric_b, metric_c, metric_d = st.columns(4)
metric_a.metric("Total baris", f"{len(df):,}".replace(",", "."))
metric_b.metric("Total penjualan", rupiah(df["total_penjualan"].sum()))
metric_c.metric("Rata-rata transaksi", rupiah(df["total_penjualan"].mean()))
metric_d.metric("Produk", df["id_produk"].nunique())

st.subheader("Tren penjualan harian")
st.line_chart(daily_sales, x="tanggal", y="total_penjualan", height=320)

left, right = st.columns(2)
with left:
    st.subheader("Penjualan per kategori")
    st.bar_chart(category_sales, x="kategori_produk", y="total_penjualan", height=280)

with right:
    st.subheader("Rata-rata penjualan saat promo")
    promo_sales["status_promo"] = promo_sales["promo_aktif"].map({0: "Tanpa promo", 1: "Promo"})
    st.bar_chart(promo_sales, x="status_promo", y="total_penjualan", height=280)

st.subheader("Cuplikan dataset")
st.dataframe(df.head(120), use_container_width=True)
