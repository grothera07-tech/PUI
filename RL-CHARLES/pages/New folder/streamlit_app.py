import streamlit as st

st.set_page_config(
    page_title="Prediksi Penjualan UMKM",
    page_icon="RF",
    layout="wide",
)

pages = [
    st.Page("pages/1_Dashboard_Data.py", title="Dashboard Data"),
    st.Page("pages/2_Prediksi_Penjualan.py", title="Prediksi Penjualan"),
    st.Page("pages/3_Evaluasi_Model.py", title="Evaluasi Model"),
]

navigation = st.navigation(pages)
navigation.run()
