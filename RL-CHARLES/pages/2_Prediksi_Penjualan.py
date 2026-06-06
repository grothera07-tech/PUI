import pandas as pd
import streamlit as st
from src.app_utils import is_ramadan_lebaran, load_data, model_ready, predict_sales, rupiah
from src.ui_components import hero_section, section_header, status_badge, render_status_pills

st.set_page_config(page_title="Prediksi Penjualan", layout="wide")

ready = model_ready()
badge_class, badge_text = status_badge(ready, "Prediction workflow ready", "Model atau dataset belum siap")
hero_section("Guided Prediction Workflow", "Prediksi Penjualan Harian", "", badge_class, badge_text)

if not ready:
    st.warning("Dataset atau model belum tersedia. Jalankan generator dataset dan training model terlebih dahulu.")
    st.stop()

df = load_data()

left_col, right_col = st.columns([1.35, 0.95], gap="large")

with left_col:
    section_header("Input Configuration", "Setup Scenario", "")

    # Product details section
    with st.container(border=True):
        section_header("Product Info", "Product Details", "")
        selected_product = st.selectbox("Produk", sorted(df["nama_produk"].unique()))
        product_rows = df[df["nama_produk"] == selected_product]
        selected_date = st.date_input("Tanggal", pd.Timestamp("2025-07-01"))
        
        product_a, product_b = st.columns(2)
        with product_a:
            harga_satuan = st.number_input(
                "Harga satuan",
                min_value=1000,
                max_value=250000,
                value=int(product_rows["harga_satuan"].median()),
                step=500,
            )
        with product_b:
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

    # Sales parameters section
    with st.container(border=True):
        section_header("Sales Condition", "Sales Parameters", "")
        promo_aktif = st.toggle("Promo aktif", value=False)
        diskon_persen = st.slider("Diskon persen", 0, 30, 10 if promo_aktif else 0, step=5)
        kanal_penjualan = st.selectbox("Kanal penjualan", sorted(df["kanal_penjualan"].unique()))
        jumlah_pengunjung = st.number_input("Estimasi pengunjung", min_value=10, max_value=300, value=110, step=5)

    # External factors section
    with st.container(border=True):
        section_header("External Factor", "External Factors", "")
        cuaca = st.selectbox("Cuaca", sorted(df["cuaca"].unique()))


# Build prediction input
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

# Build scenario badges
badges = []
if input_row["promo_aktif"] == 1:
    badges.append("🎉 Promo aktif")
else:
    badges.append("🏷️ Tanpa promo")

if input_row["akhir_pekan"] == 1:
    badges.append("📅 Akhir pekan")
else:
    badges.append("📅 Hari kerja")

if input_row["musim_ramadan_lebaran"] == 1:
    badges.append("🌙 Ramadan/Lebaran")

if input_row["jumlah_pengunjung"] >= 150:
    badges.append("🚀 Traffic tinggi")

# Premium result panel on right
with right_col:
    section_header("Result Panel", "Prediction Result", "")
    
    st.markdown(
        f"""
        <div class="result-panel">
            <div class="result-kicker">💰 Prediksi total penjualan</div>
            <div class="result-number">{rupiah(prediction)}</div>
            <div style="margin-top:0.95rem;">{render_status_pills(badges)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick summary
    with st.container(border=True):
        section_header("Quick Summary", "Scenario Context", "")
        summary_left, summary_right = st.columns(2)
        
        with summary_left:
            st.markdown(f"**Produk**  \n{input_row['nama_produk']}")
            st.markdown(f"**Kategori**  \n{input_row['kategori_produk']}")
            st.markdown(f"**Harga satuan**  \n{rupiah(input_row['harga_satuan'])}")
            st.markdown(f"**Stok awal**  \n{input_row['stok_awal']}")
            st.markdown(f"**Rating produk**  \n{input_row['rating_produk']:.1f}")
        
        with summary_right:
            st.markdown(f"**Tanggal**  \n{selected_date}")
            st.markdown(f"**Kanal penjualan**  \n{input_row['kanal_penjualan']}")
            st.markdown(f"**Cuaca**  \n{input_row['cuaca']}")
            st.markdown(f"**Pengunjung**  \n{input_row['jumlah_pengunjung']}")
            st.markdown(f"**Diskon**  \n{input_row['diskon_persen']}%")

# Detailed summary table
result = pd.DataFrame([input_row])
result["prediksi_total_penjualan"] = int(round(prediction, 0))

summary_df = pd.DataFrame(
    {
        "Parameter": [
            "Produk",
            "Kategori",
            "Tanggal",
            "Harga satuan",
            "Stok awal",
            "Diskon persen",
            "Promo aktif",
            "Kanal penjualan",
            "Hari dalam minggu",
            "Akhir pekan",
            "Bulan",
            "Musim Ramadan/Lebaran",
            "Cuaca",
            "Jumlah pengunjung",
            "Rating produk",
            "Prediksi total penjualan",
        ],
        "Nilai": [
            result.loc[0, "nama_produk"],
            result.loc[0, "kategori_produk"],
            str(selected_date),
            rupiah(result.loc[0, "harga_satuan"]),
            int(result.loc[0, "stok_awal"]),
            f"{int(result.loc[0, 'diskon_persen'])}%",
            "Ya" if int(result.loc[0, "promo_aktif"]) == 1 else "Tidak",
            result.loc[0, "kanal_penjualan"],
            result.loc[0, "hari_dalam_minggu"],
            "Ya" if int(result.loc[0, "akhir_pekan"]) == 1 else "Tidak",
            int(result.loc[0, "bulan"]),
            "Ya" if int(result.loc[0, "musim_ramadan_lebaran"]) == 1 else "Tidak",
            result.loc[0, "cuaca"],
            int(result.loc[0, "jumlah_pengunjung"]),
            float(result.loc[0, "rating_produk"]),
            rupiah(result.loc[0, "prediksi_total_penjualan"]),
        ],
    }
)

with st.container(border=True):
    section_header("Detailed Summary", "Complete I/O", "")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

with st.expander("Lihat struktur data model yang dikirim ke prediksi", expanded=False):
    st.dataframe(result, use_container_width=True)

