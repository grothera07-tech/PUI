# Sistem Prediksi Penjualan UMKM Menggunakan Random Forest

Prototype Proyek Utama Informatika untuk prediksi `total_penjualan` harian UMKM umum memakai Random Forest Regression.

## Isi Proyek

- `data/dummy_penjualan_umkm.csv`: dataset dummy sintetis.
- `notebooks/prediksi_penjualan_umkm_random_forest.ipynb`: notebook eksperimen.
- `src/generate_dummy_dataset.py`: generator dataset.
- `src/train_model.py`: training, evaluasi, dan simpan model.
- `streamlit_app.py` + `pages/`: aplikasi Streamlit multipage.
- `reports/`: metrik, prediksi test, feature importance, dan laporan akademik.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Jalankan Pipeline

```bash
python src/generate_dummy_dataset.py
python src/train_model.py
python src/build_notebook.py
python src/build_report.py
libreoffice --headless --convert-to pdf --outdir reports reports/laporan_proyek_utama_informatika.docx
```

## Jalankan Streamlit

```bash
streamlit run streamlit_app.py
```

## Catatan Akademik

Dataset sepenuhnya sintetis dan aman untuk prototype. Untuk tahap profesional, ganti dataset dengan transaksi POS asli, validasi kualitas data, lakukan retraining berkala, dan pantau error prediksi.
