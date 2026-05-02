# Sistem Prediksi Penjualan Produk UMKM Menggunakan Random Forest

## Deskripsi Project

Sistem prediksi penjualan produk UMKM menggunakan algoritma Random Forest untuk memprediksi volume penjualan berdasarkan fitur-fitur historis dan data terkini. Project ini dirancang untuk membantu UMKM dalam forecasting penjualan dan membuat keputusan bisnis yang lebih baik.

## Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd Project
```

### 2. Setup Virtual Environment
```bash
# Menggunakan setup.sh (Linux/Mac/Git Bash)
bash setup.sh

# Atau manual setup (Windows)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Cara Menjalankan Aplikasi

Jalankan aplikasi Streamlit dengan command:
```bash
streamlit run app/main.py
```

Aplikasi akan membuka di browser pada alamat `http://localhost:8501`

## Struktur Folder

```
Project/
├── data/
│   ├── raw/                  # Dataset mentah (input)
│   └── processed/            # Dataset hasil preprocessing
├── model/                    # Model yang sudah dilatih (.joblib)
├── notebooks/                # Jupyter notebook untuk EDA & eksperimen
├── app/                      # Kode aplikasi Streamlit
│   └── main.py              # Entry point aplikasi
├── docs/                     # Dokumentasi & screenshot
├── utils/                    # Helper functions
│   ├── preprocessing.py      # Data preprocessing & feature engineering
│   └── __init__.py
├── requirements.txt          # Python dependencies
├── setup.sh                  # Script setup otomatis
├── .gitignore               # Git ignore rules
└── README.md                # File ini
```

## Requirements

Berikut adalah library yang digunakan:
- scikit-learn: Machine Learning library
- pandas: Data manipulation
- numpy: Numerical computing
- matplotlib: Plotting
- seaborn: Statistical visualization
- streamlit: Web app framework
- joblib: Model serialization
- openpyxl: Excel file handling

## Kontribusi

Silakan fork repository ini dan buat pull request untuk kontribusi.

## License

MIT License