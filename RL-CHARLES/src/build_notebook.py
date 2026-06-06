from __future__ import annotations

from pathlib import Path

import nbformat as nbf


NOTEBOOK_PATH = Path("notebooks/prediksi_penjualan_umkm_random_forest.ipynb")


def md(text: str):
    return nbf.v4.new_markdown_cell(text)


def code(text: str):
    return nbf.v4.new_code_cell(text)


def build_notebook() -> None:
    nb = nbf.v4.new_notebook()
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    nb["cells"] = [
        md("# Sistem Prediksi Penjualan UMKM Menggunakan Random Forest\n\nNotebook ini berisi alur eksperimen terstruktur untuk prototype Proyek Utama Informatika."),
        md("## 1. Tujuan\n\nMemprediksi `total_penjualan` harian UMKM umum menggunakan Random Forest Regression pada dataset dummy sintetis yang aman."),
        code("import json\nfrom pathlib import Path\n\nimport joblib\nimport matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns"),
        md("## 2. Load Dataset"),
        code("DATA_PATH = Path('../data/dummy_penjualan_umkm.csv')\ndf = pd.read_csv(DATA_PATH, parse_dates=['tanggal'])\ndf.head()"),
        code("df.info()\ndf.describe(include='all').T.head(20)"),
        md("## 3. Validasi Data\n\nCek nilai kosong, target negatif, dan rentang tanggal."),
        code("print('Missing values:')\nprint(df.isna().sum())\nprint('Target negatif:', (df['total_penjualan'] < 0).sum())\nprint(df['tanggal'].min(), df['tanggal'].max())"),
        md("## 4. Exploratory Data Analysis"),
        code("daily_sales = df.groupby('tanggal')['total_penjualan'].sum()\nplt.figure(figsize=(12, 4))\ndaily_sales.plot()\nplt.title('Tren Total Penjualan Harian')\nplt.ylabel('Total penjualan')\nplt.tight_layout()\nplt.show()"),
        code("category_sales = df.groupby('kategori_produk')['total_penjualan'].sum().sort_values(ascending=False)\nplt.figure(figsize=(8, 4))\ncategory_sales.plot(kind='bar')\nplt.title('Total Penjualan per Kategori')\nplt.ylabel('Total penjualan')\nplt.tight_layout()\nplt.show()"),
        code("plt.figure(figsize=(7, 4))\nsns.boxplot(data=df, x='promo_aktif', y='total_penjualan')\nplt.title('Distribusi Penjualan Berdasarkan Status Promo')\nplt.tight_layout()\nplt.show()"),
        md("## 5. Pemodelan\n\nTraining dilakukan melalui script `src/train_model.py`. Fitur pasca transaksi seperti `jumlah_terjual`, `stok_akhir`, dan `biaya_promosi` tidak dipakai agar tidak terjadi data leakage."),
        code("import sys\nsys.path.append('..')\nfrom src.train_model import FEATURES, TARGET, build_pipeline, evaluate, load_dataset, split_by_time\n\ndf = load_dataset(Path('../data/dummy_penjualan_umkm.csv'))\ntrain_df, test_df = split_by_time(df)\nX_train, y_train = train_df[FEATURES], train_df[TARGET]\nX_test, y_test = test_df[FEATURES], test_df[TARGET]\n\nmodel = build_pipeline()\nmodel.fit(X_train, y_train)\npred = model.predict(X_test)\nevaluate(y_test, pred)"),
        md("## 6. Load Artefak Training"),
        code("MODEL_PATH = Path('../models/random_forest_penjualan_umkm.joblib')\nMETRICS_PATH = Path('../reports/model_metrics.json')\nIMPORTANCE_PATH = Path('../reports/feature_importance.csv')\n\nbundle = joblib.load(MODEL_PATH)\nmetrics = json.loads(METRICS_PATH.read_text())\nimportance = pd.read_csv(IMPORTANCE_PATH)\nmetrics"),
        code("importance.head(15)"),
        code("plt.figure(figsize=(9, 5))\nsns.barplot(data=importance.head(12), y='feature', x='importance')\nplt.title('Feature Importance Random Forest')\nplt.tight_layout()\nplt.show()"),
        md("## 7. Interpretasi\n\nMetrik menunjukkan performa pada dataset dummy. Kesimpulan tidak boleh digeneralisasi ke UMKM nyata sebelum validasi memakai data transaksi asli."),
        md("## 8. Saran Lanjutan\n\nGunakan data POS asli, buat validasi data, lakukan perbandingan model, dan monitoring error setelah sistem dipakai."),
    ]
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    nbf.write(nb, NOTEBOOK_PATH)
    print(f"saved {NOTEBOOK_PATH}")


if __name__ == "__main__":
    build_notebook()
