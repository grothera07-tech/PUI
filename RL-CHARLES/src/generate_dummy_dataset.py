from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
DEFAULT_OUTPUT = Path("data/dummy_penjualan_umkm.csv")


@dataclass(frozen=True)
class Product:
    id_produk: str
    nama_produk: str
    kategori_produk: str
    harga_dasar: int
    permintaan_dasar: float
    elastisitas_harga: float
    rating_dasar: float


PRODUCTS = [
    Product("P001", "Paket nasi lauk", "makanan_minuman", 18000, 28, 0.35, 4.5),
    Product("P002", "Minuman kopi susu", "makanan_minuman", 15000, 32, 0.30, 4.4),
    Product("P003", "Snack kemasan lokal", "makanan_minuman", 9000, 38, 0.25, 4.2),
    Product("P004", "Kaos basic", "fashion", 65000, 9, 0.55, 4.3),
    Product("P005", "Hijab polos", "fashion", 42000, 13, 0.45, 4.5),
    Product("P006", "Sandal harian", "fashion", 55000, 8, 0.50, 4.1),
    Product("P007", "Sabun cuci literan", "kebutuhan_rumah", 17000, 20, 0.25, 4.2),
    Product("P008", "Beras 5 kg", "kebutuhan_rumah", 72000, 11, 0.20, 4.6),
    Product("P009", "Minyak goreng 1 liter", "kebutuhan_rumah", 19000, 22, 0.25, 4.4),
    Product("P010", "Aksesori ponsel", "aksesoris", 25000, 16, 0.60, 4.0),
    Product("P011", "Buket mini", "kerajinan", 45000, 7, 0.40, 4.7),
    Product("P012", "Paket hampers", "kerajinan", 95000, 5, 0.55, 4.6),
]


WEATHER_EFFECT = {
    "cerah": 1.08,
    "berawan": 1.00,
    "hujan_ringan": 0.90,
    "hujan_deras": 0.78,
}

CHANNEL_EFFECT = {
    "offline": 1.00,
    "online": 0.92,
    "campuran": 1.12,
}


def _is_ramadan_lebaran(date: pd.Timestamp) -> int:
    periods = [
        (pd.Timestamp("2024-03-12"), pd.Timestamp("2024-04-20")),
        (pd.Timestamp("2025-03-01"), pd.Timestamp("2025-04-10")),
    ]
    return int(any(start <= date <= end for start, end in periods))


def _category_season_boost(category: str, month: int, ramadan: int) -> float:
    if category == "fashion" and (ramadan or month in [6, 12]):
        return 1.28
    if category == "makanan_minuman" and ramadan:
        return 1.18
    if category == "kerajinan" and month in [2, 4, 12]:
        return 1.35
    if category == "kebutuhan_rumah" and month in [1, 7, 12]:
        return 1.10
    return 1.00


def _sample_weather(rng: np.random.Generator, month: int) -> str:
    values = ["cerah", "berawan", "hujan_ringan", "hujan_deras"]
    if month in [1, 2, 3, 11, 12]:
        probs = [0.22, 0.28, 0.32, 0.18]
    else:
        probs = [0.48, 0.31, 0.16, 0.05]
    return str(rng.choice(values, p=probs))


def generate_dataset(
    output_path: Path | str = DEFAULT_OUTPUT,
    start_date: str = "2024-01-01",
    end_date: str = "2025-06-30",
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    rows: list[dict[str, object]] = []

    for date in dates:
        day_name = date.day_name()
        akhir_pekan = int(day_name in ["Saturday", "Sunday"])
        month = int(date.month)
        ramadan_lebaran = _is_ramadan_lebaran(date)
        weather = _sample_weather(rng, month)

        visitor_base = 95 + (35 if akhir_pekan else 0) + (18 if ramadan_lebaran else 0)
        visitor_weather = WEATHER_EFFECT[weather]
        daily_visitors = max(20, int(rng.normal(visitor_base * visitor_weather, 14)))

        for product in PRODUCTS:
            promo_aktif = int(rng.random() < (0.28 if akhir_pekan else 0.16))
            diskon_persen = int(rng.choice([5, 10, 15, 20], p=[0.40, 0.35, 0.20, 0.05])) if promo_aktif else 0
            kanal_penjualan = str(rng.choice(["offline", "online", "campuran"], p=[0.46, 0.29, 0.25]))

            harga_noise = rng.normal(1.0, 0.035)
            harga_satuan = int(round(product.harga_dasar * harga_noise / 500) * 500)
            harga_ratio = max(0.65, min(1.35, harga_satuan / product.harga_dasar))
            price_effect = max(0.55, 1 - product.elastisitas_harga * (harga_ratio - 1))

            promo_effect = 1 + (0.32 + diskon_persen / 100) * promo_aktif
            weekend_effect = 1.22 if akhir_pekan else 0.96
            season_effect = _category_season_boost(product.kategori_produk, month, ramadan_lebaran)
            channel_effect = CHANNEL_EFFECT[kanal_penjualan]
            traffic_effect = 0.82 + min(daily_visitors, 170) / 230
            weather_effect = WEATHER_EFFECT[weather]

            expected_units = (
                product.permintaan_dasar
                * promo_effect
                * weekend_effect
                * season_effect
                * channel_effect
                * traffic_effect
                * weather_effect
                * price_effect
            )
            expected_units = max(1.0, expected_units)

            stok_awal = int(max(3, rng.normal(expected_units * 1.55, expected_units * 0.25)))
            jumlah_terjual = int(min(stok_awal, rng.poisson(expected_units)))
            stok_akhir = stok_awal - jumlah_terjual
            harga_setelah_diskon = harga_satuan * (1 - diskon_persen / 100)
            total_penjualan = int(round(jumlah_terjual * harga_setelah_diskon, -2))
            rating_produk = round(float(np.clip(rng.normal(product.rating_dasar, 0.15), 3.4, 5.0)), 1)
            biaya_promosi = int(round((diskon_persen / 100) * harga_satuan * max(jumlah_terjual, 1), -2))

            rows.append(
                {
                    "tanggal": date.strftime("%Y-%m-%d"),
                    "id_produk": product.id_produk,
                    "nama_produk": product.nama_produk,
                    "kategori_produk": product.kategori_produk,
                    "harga_satuan": harga_satuan,
                    "stok_awal": stok_awal,
                    "stok_akhir": stok_akhir,
                    "jumlah_terjual": jumlah_terjual,
                    "total_penjualan": total_penjualan,
                    "diskon_persen": diskon_persen,
                    "promo_aktif": promo_aktif,
                    "biaya_promosi": biaya_promosi,
                    "kanal_penjualan": kanal_penjualan,
                    "hari_dalam_minggu": day_name,
                    "akhir_pekan": akhir_pekan,
                    "bulan": month,
                    "musim_ramadan_lebaran": ramadan_lebaran,
                    "cuaca": weather,
                    "jumlah_pengunjung": daily_visitors,
                    "rating_produk": rating_produk,
                }
            )

    df = pd.DataFrame(rows)
    df = df.sort_values(["tanggal", "id_produk"]).reset_index(drop=True)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return df


if __name__ == "__main__":
    dataset = generate_dataset()
    print(f"saved {DEFAULT_OUTPUT} with {len(dataset):,} rows and {len(dataset.columns)} columns")
