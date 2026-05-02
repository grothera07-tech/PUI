import streamlit as st
import joblib
import pandas as pd
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Sistem Prediksi Penjualan UMKM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model
@st.cache_resource
def load_model():
    """Load trained model if exists"""
    model_path = Path("model") / "model.joblib"
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

# Page title
st.title("📊 Sistem Prediksi Penjualan UMKM")
st.markdown("Aplikasi prediksi penjualan produk UMKM menggunakan Random Forest")

# Sidebar navigation
st.sidebar.title("🔍 Navigasi")
page = st.sidebar.radio(
    "Pilih halaman:",
    ["Upload Data", "Prediksi", "Analisis Model"]
)

# Load model once
model = load_model()

# Page: Upload Data
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

# Page: Prediksi
elif page == "Prediksi":
    st.header("🎯 Prediksi Penjualan")
    st.markdown("---")
    
    if model is not None:
        st.write("Masukkan fitur-fitur untuk melakukan prediksi penjualan.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            feature1 = st.number_input("Fitur 1:", value=0.0)
        
        with col2:
            feature2 = st.number_input("Fitur 2:", value=0.0)
        
        if st.button("🔮 Prediksi"):
            try:
                # Placeholder untuk prediksi
                st.info("Fitur prediksi akan diimplementasikan setelah model tersedia")
            except Exception as e:
                st.error(f"❌ Error dalam prediksi: {str(e)}")
    else:
        st.warning("⚠️ Model belum tersedia untuk melakukan prediksi.")

# Page: Analisis Model
elif page == "Analisis Model":
    st.header("📈 Analisis Model")
    st.markdown("---")
    
    if model is not None:
        st.write("Analisis performa dan karakteristik model Random Forest.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Status Model", "✅ Loaded")
        
        with col2:
            st.metric("Tipe Model", "Random Forest")
        
        st.subheader("📊 Feature Importance")
        st.write("Placeholder untuk visualisasi feature importance")
        
        st.subheader("📉 Model Performance")
        st.write("Placeholder untuk metrik performa model")
        
    else:
        st.warning("⚠️ Model belum tersedia untuk dianalisis.")

st.markdown("---")
st.caption("© 2024 Sistem Prediksi Penjualan UMKM | Powered by Streamlit")
