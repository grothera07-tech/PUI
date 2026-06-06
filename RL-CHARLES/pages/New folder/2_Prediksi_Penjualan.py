import pandas as pd
import streamlit as st

from src.app_utils import is_ramadan_lebaran, load_data, model_ready, predict_sales, rupiah


st.title("Prediksi Penjualan Harian")

if not model_ready():
    st.warning("Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu.")
    st.stop()

df = load_data()

left, right = st.columns(2)

with left:
    selected_product = st.selectbox("Produk", sorted(df["nama_produk"].unique()))
    product_rows = df[df["nama_produk"] == selected_product]
    selected_date = st.date_input("Tanggal", pd.Timestamp("2025-07-01"))
    harga_satuan = st.number_input(
        "Harga satuan",
        min_value=1000,
        max_value=250000,
        value=int(product_rows["harga_satuan"].median()),
        step=500,
    )
    stok_awal = st.number_input(
        "Stok awal",
        min_value=0,
        max_value=300,
        value=int(product_rows["stok_awal"].median()),
        step=1,
    )
    rating_produk = st.slider(
        "Rating produk",
        min_value=3.0,
        max_value=5.0,
        value=float(product_rows["rating_produk"].median()),
        step=0.1,
    )

with right:
    promo_aktif = st.toggle("Promo aktif", value=False)
    diskon_persen = st.slider("Diskon persen", 0, 30, 10 if promo_aktif else 0, step=5)
    kanal_penjualan = st.selectbox("Kanal penjualan", sorted(df["kanal_penjualan"].unique()))
    cuaca = st.selectbox("Cuaca", sorted(df["cuaca"].unique()))
    jumlah_pengunjung = st.number_input("Estimasi pengunjung", min_value=10, max_value=300, value=110, step=5)

date = pd.Timestamp(selected_date)
input_row = {
    "nama_produk": selected_product,
    "kategori_produk": str(product_rows["kategori_produk"].mode().iloc[0]),
    "harga_satuan": int(harga_satuan),
    "stok_awal": int(stok_awal),
    "diskon_persen": int(diskon_persen if promo_aktif else 0),
    "promo_aktif": int(promo_aktif),
    "kanal_penjualan": kanal_penjualan,
    "hari_dalam_minggu": date.day_name(),
    "akhir_pekan": int(date.day_name() in ["Saturday", "Sunday"]),
    "bulan": int(date.month),
    "musim_ramadan_lebaran": is_ramadan_lebaran(date),
    "cuaca": cuaca,
    "jumlah_pengunjung": int(jumlah_pengunjung),
    "rating_produk": float(rating_produk),
}

prediction = max(0, predict_sales(input_row))

st.divider()
st.metric("Prediksi total penjualan", rupiah(prediction))

result = pd.DataFrame([input_row])
result["prediksi_total_penjualan"] = int(round(prediction, 0))
st.dataframe(result, use_container_width=True)
