"""
Script untuk generate sample dataset penjualan UMKM
untuk keperluan testing dan development EDA

Output: data/raw/penjualan_umkm.csv
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# Set random seed untuk reproducibility
np.random.seed(42)
random.seed(42)

print("=" * 80)
print("🔧 GENERATE SAMPLE DATASET PENJUALAN UMKM")
print("=" * 80)

# =====================================================================
# 1. SETUP: Definisikan data yang akan di-generate
# =====================================================================

# Daftar produk (minimal 10 item)
PRODUK_DATA = {
    'Minuman': [
        {'nama': 'Kopi Susu', 'harga': 12000},
        {'nama': 'Es Teh Manis', 'harga': 8000},
        {'nama': 'Jus Alpukat', 'harga': 15000},
        {'nama': 'Susu Coklat', 'harga': 14000},
    ],
    'Makanan': [
        {'nama': 'Nasi Goreng', 'harga': 25000},
        {'nama': 'Mie Ayam', 'harga': 20000},
        {'nama': 'Ayam Geprek', 'harga': 28000},
        {'nama': 'Nasi Uduk', 'harga': 22000},
    ],
    'Snack': [
        {'nama': 'Roti Bakar', 'harga': 18000},
        {'nama': 'Pisang Goreng', 'harga': 10000},
        {'nama': 'Kentang Goreng', 'harga': 12000},
    ]
}

LOKASI = ['Cabang A', 'Cabang B', 'Cabang C']
METODE_PEMBAYARAN = ['Cash', 'QRIS', 'Transfer', 'E-Wallet']

# Distribusi metode pembayaran (%)
PEMBAYARAN_DIST = {
    'Cash': 0.60,
    'QRIS': 0.20,
    'Transfer': 0.10,
    'E-Wallet': 0.10
}

print("\n📋 KONFIGURASI GENERATE DATA:")
print(f"  • Periode: 1 Januari 2023 - 31 Desember 2024 (2 tahun)")
print(f"  • Target baris: 1000+ transaksi")
print(f"  • Jumlah produk unik: {sum(len(produk) for produk in PRODUK_DATA.values())}")
print(f"  • Lokasi: {len(LOKASI)} cabang")
print(f"  • Metode pembayaran: {len(METODE_PEMBAYARAN)} metode")

# =====================================================================
# 2. GENERATE BASELINE DATA
# =====================================================================

print("\n⏳ Generating baseline data...")

# Setup periode
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

# Generate data
data = []

for current_date in all_dates:
    # Tentukan jumlah transaksi per hari
    day_of_week = current_date.weekday()  # 0=Senin, 6=Minggu
    month = current_date.month
    
    # Weekend (Sabtu=5, Minggu=6) lebih tinggi
    if day_of_week >= 5:  # Sabtu atau Minggu
        n_transactions = np.random.randint(8, 15)  # 8-15 transaksi
    else:
        n_transactions = np.random.randint(4, 10)  # 4-10 transaksi
    
    # Musiman: Desember dan Ramadhan (Maret-April) lebih tinggi
    if month == 12 or month in [3, 4]:
        n_transactions = int(n_transactions * 1.5)
    
    # Generate transaksi untuk hari ini
    for _ in range(n_transactions):
        # Pilih kategori produk dengan bias ke Minuman
        category = np.random.choice(
            list(PRODUK_DATA.keys()),
            p=[0.5, 0.3, 0.2]  # Minuman 50%, Makanan 30%, Snack 20%
        )
        
        # Pilih produk random dari kategori
        produk_list = PRODUK_DATA[category]
        produk = random.choice(produk_list)
        
        # Generate jumlah terjual (rata-rata 5, dengan outlier)
        if random.random() < 0.05:  # 5% outlier
            jumlah = np.random.randint(200, 500)  # Outlier ekstrim
        else:
            jumlah = np.random.randint(1, 50)
        
        # Harga satuan
        harga = produk['harga']
        
        # Total penjualan
        total = jumlah * harga
        
        # Lokasi random
        lokasi = random.choice(LOKASI)
        
        # Metode pembayaran (sesuai distribusi)
        metode = np.random.choice(
            list(METODE_PEMBAYARAN),
            p=[PEMBAYARAN_DIST[m] for m in METODE_PEMBAYARAN]
        )
        
        data.append({
            'tanggal': current_date.date(),
            'nama_produk': produk['nama'],
            'kategori_produk': category,
            'jumlah_terjual': jumlah,
            'harga_satuan': harga,
            'total_penjualan': total,
            'lokasi': lokasi,
            'metode_pembayaran': metode
        })

# Buat DataFrame
df = pd.DataFrame(data)

print(f"✅ Generated {len(df)} transaksi")

# =====================================================================
# 3. TAMBAHKAN MISSING VALUES (5-10 baris)
# =====================================================================

print("\n🔧 Menambahkan missing values...")

n_missing = random.randint(5, 10)
missing_indices = np.random.choice(df.index, size=n_missing, replace=False)
missing_columns = random.sample(list(df.columns), k=2)

for idx in missing_indices:
    col = random.choice(missing_columns)
    df.loc[idx, col] = np.nan

print(f"✅ Ditambahkan {n_missing} baris dengan missing values di kolom: {missing_columns}")

# =====================================================================
# 4. TAMBAHKAN DUPLIKAT (3-5 baris)
# =====================================================================

print("\n🔧 Menambahkan duplikat...")

n_duplicate = random.randint(3, 5)
duplicate_indices = np.random.choice(df.index, size=n_duplicate, replace=False)
duplicate_rows = df.loc[duplicate_indices].copy()
df = pd.concat([df, duplicate_rows], ignore_index=True)

print(f"✅ Ditambahkan {n_duplicate} baris duplikat")

# =====================================================================
# 5. SHUFFLE DATA
# =====================================================================

print("\n🔄 Shuffling data...")

df = df.sample(frac=1).reset_index(drop=True)

# =====================================================================
# 6. BUAT FOLDER OUTPUT JIKA BELUM ADA
# =====================================================================

output_dir = Path('../data/raw')
output_dir.mkdir(parents=True, exist_ok=True)

# =====================================================================
# 7. SIMPAN KE CSV
# =====================================================================

output_path = output_dir / 'penjualan_umkm.csv'

try:
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ File berhasil tersimpan: {output_path}")
except Exception as e:
    print(f"\n❌ Error saat menyimpan file: {e}")
    exit(1)

# =====================================================================
# 8. PRINT PREVIEW & INFO
# =====================================================================

print("\n" + "=" * 80)
print("📊 PREVIEW DATA (10 BARIS PERTAMA)")
print("=" * 80)
print(df.head(10).to_string())

print("\n" + "=" * 80)
print("📈 INFORMASI DATASET")
print("=" * 80)
print(f"\n📌 Dimensi: {df.shape[0]} baris × {df.shape[1]} kolom")

print("\n📋 Tipe Data:")
print(df.dtypes)

print("\n📊 Statistik Numerik:")
print(df.describe().round(2))

print("\n🔍 Missing Values:")
missing = df.isnull().sum()
if missing.sum() > 0:
    print(missing[missing > 0])
else:
    print("  Tidak ada (sudah ditambahkan sengaja untuk latihan)")

print("\n🔄 Duplikat:")
n_duplikat = df.duplicated().sum()
print(f"  Total baris duplikat: {n_duplikat}")

print("\n📦 Distribusi Kategori Produk:")
print(df['kategori_produk'].value_counts())

print("\n🏪 Distribusi Lokasi:")
print(df['lokasi'].value_counts())

print("\n💳 Distribusi Metode Pembayaran:")
print(df['metode_pembayaran'].value_counts())

print("\n📈 Statistik Penjualan:")
print(f"  • Total penjualan: Rp {df['total_penjualan'].sum():,.0f}")
print(f"  • Rata-rata transaksi: Rp {df['total_penjualan'].mean():,.0f}")
print(f"  • Min: Rp {df['total_penjualan'].min():,.0f}")
print(f"  • Max: Rp {df['total_penjualan'].max():,.0f}")

print("\n" + "=" * 80)
print("✅ GENERATE SELESAI!")
print("=" * 80)
print(f"\n📁 File output: {output_path.resolve()}")
print(f"📊 Dataset siap untuk EDA di notebook 01_eda.ipynb")
print(f"\n💡 Tips: Update path di cell 2 notebook menjadi:")
print(f"   data_path = '../data/raw/penjualan_umkm.csv'")
print("\n" + "=" * 80)
