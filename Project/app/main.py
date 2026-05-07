import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import date
import sys
import os

# Tambahkan path utils agar bisa import preprocessing
sys.path.append(str(Path(__file__).parent.parent))
from utils.preprocessing import (
    load_data, clean_data, handle_outliers,
    encode_features, create_time_features, split_data
)

# =============================================
# KONFIGURASI HALAMAN
# =============================================
st.set_page_config(
    page_title="Sistem Prediksi Penjualan UMKM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# LOAD MODEL
# =============================================
@st.cache_resource
def load_model():
    """Load trained model jika ada."""
    model_path = Path(__file__).parent.parent / "model" / "rf_model.pkl"
    try:
        if model_path.exists():
            model = joblib.load(model_path)
            return model
        else:
            st.warning("⚠️ Model belum tersedia. Silakan latih model terlebih dahulu.")
            return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

# =============================================
# HEADER UTAMA
# =============================================
st.title("📊 Sistem Prediksi Penjualan UMKM")
st.markdown("Aplikasi prediksi penjualan produk UMKM menggunakan Random Forest")

# =============================================
# SIDEBAR NAVIGASI
# =============================================
st.sidebar.title("🔍 Navigasi")
page = st.sidebar.radio(
    "Pilih halaman:",
    ["Upload Data", "Prediksi", "Analisis Model"]
)

# Load model sekali
model = load_model()

# =============================================
# HALAMAN 1: UPLOAD DATA
# =============================================
if page == "Upload Data":
    st.header("📤 Upload Data")
    st.markdown("---")
    st.write("Upload dataset Anda untuk dilakukan preprocessing dan analisis.")

    uploaded_file = st.file_uploader(
        "Pilih file (CSV atau Excel):",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File berhasil diupload!")
            st.dataframe(df, use_container_width=True)
            st.write(f"**Dataset shape:** {df.shape[0]} baris, {df.shape[1]} kolom")
            st.write(f"**Statistik deskriptif:**")
            st.dataframe(df.describe(), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# =============================================
# HALAMAN 2: PREDIKSI
# =============================================
elif page == "Prediksi":
    st.header("🎯 Prediksi Penjualan")
    st.markdown("---")

    if model is not None:
        st.write("Masukkan data produk untuk memprediksi jumlah penjualan.")

        col1, col2 = st.columns(2)

        with col1:
            # Input Nama Produk (dropdown)
            nama_produk = st.selectbox(
                "🛍️ Nama Produk:",
                options=["Keripik Pisang", "Bolu Kukus", "Kopi Bubuk", "Oreo"]
            )

            # Input Harga
            harga = st.number_input(
                "💰 Harga Produk (Rp):",
                min_value=0,
                max_value=100000,
                value=15000,
                step=500
            )

        with col2:
            # Input Tanggal
            tanggal = st.date_input(
                "📅 Tanggal Prediksi:",
                value=date.today()
            )

        st.markdown("---")

        # Tombol Prediksi
        if st.button("🔮 Prediksi Sekarang", use_container_width=True):
            try:
                # Encode nama produk ke angka
                produk_map = {
                    "Bolu Kukus": 0,
                    "Keripik Pisang": 1,
                    "Kopi Bubuk": 2,
                    "Oreo": 3
                }
                produk_encoded = produk_map[nama_produk]

                # Ekstrak fitur waktu dari tanggal
                hari               = tanggal.day
                bulan              = tanggal.month
                tahun              = tanggal.year
                hari_dalam_minggu  = tanggal.weekday()   # 0=Senin, 6=Minggu
                is_weekend         = 1 if hari_dalam_minggu >= 5 else 0
                minggu_dalam_bulan = (hari - 1) // 7 + 1
                kuartal            = (bulan - 1) // 3 + 1

                # Susun input fitur sesuai urutan saat training
                input_features = np.array([[
                    harga,
                    produk_encoded,
                    hari,
                    bulan,
                    tahun,
                    hari_dalam_minggu,
                    is_weekend,
                    minggu_dalam_bulan,
                    kuartal
                ]])

                # Lakukan prediksi
                prediksi = model.predict(input_features)[0]

                # Tampilkan hasil
                st.success("✅ Prediksi berhasil!")

                col_res1, col_res2, col_res3 = st.columns(3)

                with col_res1:
                    st.metric(
                        label="📦 Prediksi Penjualan",
                        value=f"{int(prediksi)} unit"
                    )

                with col_res2:
                    st.metric(
                        label="💰 Estimasi Pendapatan",
                        value=f"Rp {int(prediksi * harga):,}"
                    )

                with col_res3:
                    st.metric(
                        label="🛍️ Produk",
                        value=nama_produk
                    )

                # Tabel detail input
                st.markdown("#### 📋 Detail Input yang Digunakan:")
                detail_df = pd.DataFrame({
                    "Fitur": [
                        "Nama Produk", "Harga (Rp)", "Tanggal",
                        "Hari", "Bulan", "Tahun",
                        "Hari dalam Minggu", "Weekend?",
                        "Minggu dalam Bulan", "Kuartal"
                    ],
                    "Nilai": [
                        nama_produk, f"Rp {harga:,}", str(tanggal),
                        hari, bulan, tahun,
                        hari_dalam_minggu, "Ya" if is_weekend else "Tidak",
                        minggu_dalam_bulan, kuartal
                    ]
                })
                st.dataframe(detail_df, use_container_width=True)

            except Exception as e:
                st.error(f"❌ Error dalam prediksi: {str(e)}")
                st.info("💡 Pastikan model sudah dilatih dengan fitur yang sesuai.")
    else:
        st.warning("⚠️ Model belum tersedia untuk melakukan prediksi.")

# =============================================
# HALAMAN 3: ANALISIS MODEL
# =============================================
elif page == "Analisis Model":
    st.header("📈 Analisis Model")
    st.markdown("---")

    if model is not None:
        st.write("Analisis performa dan karakteristik model Random Forest.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status Model", "✅ Loaded")
        with col2:
            st.metric("Tipe Model", "Random Forest")
        with col3:
            n_trees = model.n_estimators if hasattr(model, 'n_estimators') else "-"
            st.metric("Jumlah Pohon", f"{n_trees} trees")

        st.markdown("---")

        # =============================================
        # FEATURE IMPORTANCE
        # =============================================
        st.subheader("📊 Feature Importance")
        try:
            feature_names = [
                "harga", "nama_produk", "hari", "bulan", "tahun",
                "hari_dalam_minggu", "is_weekend", "minggu_dalam_bulan", "kuartal"
            ]

            importances = model.feature_importances_
            if len(importances) == len(feature_names):
                fi_df = pd.DataFrame({
                    "Fitur": feature_names,
                    "Importance": importances
                }).sort_values("Importance", ascending=True)

                fig, ax = plt.subplots(figsize=(10, 5))
                bars = ax.barh(fi_df["Fitur"], fi_df["Importance"], color="#1f77b4")
                ax.set_xlabel("Importance Score")
                ax.set_title("Feature Importance - Random Forest")
                ax.bar_label(bars, fmt="%.4f", padding=3)
                plt.tight_layout()
                st.pyplot(fig)

                # Fitur paling berpengaruh
                top_feature = fi_df.iloc[-1]["Fitur"]
                st.info(f"🏆 Fitur paling berpengaruh: **{top_feature}**")
            else:
                st.warning("⚠️ Jumlah fitur tidak sesuai dengan model.")
        except Exception as e:
            st.error(f"❌ Tidak bisa menampilkan Feature Importance: {str(e)}")

        st.markdown("---")

        # =============================================
        # UPLOAD DATA UNTUK EVALUASI
        # =============================================
        st.subheader("📉 Evaluasi Model")
        st.write("Upload dataset untuk melihat performa model (MAE, RMSE, R²).")

        eval_file = st.file_uploader(
            "Upload dataset evaluasi (CSV):",
            type=["csv"],
            key="eval_uploader"
        )

        if eval_file is not None:
            try:
                from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

                df_eval = pd.read_csv(eval_file)

                # Preprocessing
                df_eval, _ = encode_features(df_eval, ['nama_produk'])
                df_eval    = create_time_features(df_eval, 'tanggal')
                df_eval    = df_eval.drop(columns=['tanggal'], errors='ignore')

                feature_cols = [
                    "harga", "nama_produk", "hari", "bulan", "tahun",
                    "hari_dalam_minggu", "is_weekend", "minggu_dalam_bulan", "kuartal"
                ]
                available_cols = [c for c in feature_cols if c in df_eval.columns]

                X_eval = df_eval[available_cols]
                y_eval = df_eval['jumlah']

                y_pred = model.predict(X_eval)

                mae  = mean_absolute_error(y_eval, y_pred)
                rmse = np.sqrt(mean_squared_error(y_eval, y_pred))
                r2   = r2_score(y_eval, y_pred)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("MAE", f"{mae:.2f}", help="Rata-rata selisih prediksi vs aktual")
                with c2:
                    st.metric("RMSE", f"{rmse:.2f}", help="Akar dari rata-rata kuadrat error")
                with c3:
                    st.metric("R² Score", f"{r2:.4f}", help="1.0 = sempurna, 0 = tidak akurat")

                # Grafik Actual vs Predicted
                st.subheader("📊 Actual vs Predicted")
                fig2, ax2 = plt.subplots(figsize=(12, 4))
                ax2.plot(y_eval.values[:50], label="Aktual", marker='o', linewidth=2)
                ax2.plot(y_pred[:50], label="Prediksi", marker='s', linewidth=2, linestyle='--')
                ax2.set_title("Actual vs Predicted (50 data pertama)")
                ax2.set_xlabel("Index")
                ax2.set_ylabel("Jumlah Terjual")
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig2)

            except Exception as e:
                st.error(f"❌ Error evaluasi: {str(e)}")

    else:
        st.warning("⚠️ Model belum tersedia untuk dianalisis.")

# =============================================
# FOOTER
# =============================================
st.markdown("---")
st.caption("© 2024 Sistem Prediksi Penjualan UMKM | Powered by Streamlit")
