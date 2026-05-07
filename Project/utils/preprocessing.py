"""
Data Preprocessing and Feature Engineering Module

This module provides utility functions for loading, cleaning, and preparing data
for machine learning models.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def load_data(filepath):
    """
    Load data from CSV or Excel file.

    Parameters:
    -----------
    filepath : str
        Path to the data file (CSV or Excel format)

    Returns:
    --------
    pd.DataFrame
        Loaded dataframe

    Raises:
    -------
    FileNotFoundError
        If file does not exist
    ValueError
        If file format is not supported
    """
    import os
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File tidak ditemukan: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(filepath)
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Format file tidak didukung: {ext}. Gunakan .csv atau .xlsx")

    print(f"✅ Data berhasil dimuat: {df.shape[0]} baris, {df.shape[1]} kolom")
    return df


def clean_data(df):
    """
    Clean data by handling missing values and duplicates.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe

    Returns:
    --------
    pd.DataFrame
        Cleaned dataframe

    Notes:
    ------
    - Removes duplicate rows
    - Handles missing values (strategy depends on column type)
    """
    df = df.copy()

    # Hapus duplikat
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    if before - after > 0:
        print(f"🗑️  {before - after} baris duplikat dihapus.")
    else:
        print("✅ Tidak ada duplikat ditemukan.")

    # Tangani missing values
    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Isi missing value numerik dengan median
                df[col] = df[col].fillna(df[col].median())
                print(f"🔧 Kolom '{col}': {missing} missing values diisi dengan median.")
            else:
                # Isi missing value kategorikal dengan modus
                df[col] = df[col].fillna(df[col].mode()[0])
                print(f"🔧 Kolom '{col}': {missing} missing values diisi dengan modus.")

    print(f"✅ Data setelah cleaning: {df.shape[0]} baris, {df.shape[1]} kolom")
    return df


def handle_outliers(df, columns):
    """
    Detect and handle outliers using IQR method.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        List of column names to check for outliers

    Returns:
    --------
    pd.DataFrame
        Dataframe with outliers handled

    Notes:
    ------
    - Uses Interquartile Range (IQR) method
    - Replaces outliers with median value
    """
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            print(f"⚠️  Kolom '{col}' tidak ditemukan, dilewati.")
            continue

        if not pd.api.types.is_numeric_dtype(df[col]):
            print(f"⚠️  Kolom '{col}' bukan numerik, dilewati.")
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()

        if outliers > 0:
            # Ganti outlier dengan median
            median_val = df[col].median()
            df[col] = np.where(
                (df[col] < lower_bound) | (df[col] > upper_bound),
                median_val,
                df[col]
            )
            print(f"🔧 Kolom '{col}': {outliers} outlier diganti dengan median ({median_val:.2f})")
        else:
            print(f"✅ Kolom '{col}': Tidak ada outlier ditemukan.")

    return df


def encode_features(df, categorical_cols):
    """
    Encode categorical features using appropriate encoding methods.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    categorical_cols : list
        List of categorical column names

    Returns:
    --------
    pd.DataFrame
        Dataframe with encoded categorical features

    Notes:
    ------
    - Uses LabelEncoder untuk kolom kategorikal (nama_produk, dll)
    """
    df = df.copy()
    encoders = {}

    for col in categorical_cols:
        if col not in df.columns:
            print(f"⚠️  Kolom '{col}' tidak ditemukan, dilewati.")
            continue

        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

        classes = list(le.classes_)
        print(f"✅ Kolom '{col}' di-encode: {dict(zip(classes, range(len(classes))))}")

    return df, encoders


def create_time_features(df, date_col):
    """
    Extract time-based features from datetime column.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_col : str
        Name of the datetime column

    Returns:
    --------
    pd.DataFrame
        Dataframe with new time features (day, month, year, day_of_week, etc.)

    Notes:
    ------
    - Creates features: day, month, year, quarter, day_of_week
    - Also creates: is_weekend, minggu_dalam_bulan
    """
    df = df.copy()

    if date_col not in df.columns:
        raise ValueError(f"Kolom '{date_col}' tidak ditemukan di dataframe!")

    # Konversi ke datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Ekstrak fitur waktu
    df['hari']              = df[date_col].dt.day
    df['bulan']             = df[date_col].dt.month
    df['tahun']             = df[date_col].dt.year
    df['kuartal']           = df[date_col].dt.quarter
    df['hari_dalam_minggu'] = df[date_col].dt.dayofweek  # 0=Senin, 6=Minggu
    df['is_weekend']        = df['hari_dalam_minggu'].apply(lambda x: 1 if x >= 5 else 0)
    df['minggu_dalam_bulan']= df[date_col].apply(lambda x: (x.day - 1) // 7 + 1)

    print(f"✅ Fitur waktu berhasil dibuat dari kolom '{date_col}':")
    print(f"   → hari, bulan, tahun, kuartal, hari_dalam_minggu, is_weekend, minggu_dalam_bulan")

    return df


def create_lag_features(df, target_col, lags):
    """
    Create lag features for time series analysis.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe (must be sorted by date)
    target_col : str
        Name of the target column to create lags from
    lags : list or int
        List of lag periods or number of lags to create
        (e.g., [1, 7, 30] for 1, 7, 30 day lags)

    Returns:
    --------
    pd.DataFrame
        Dataframe with lag features

    Example:
    --------
    >>> df = pd.DataFrame({'sales': [100, 150, 200, 250]})
    >>> df_with_lags = create_lag_features(df, 'sales', lags=[1, 2])
    """
    df = df.copy()

    if target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ditemukan!")

    # Jika lags berupa integer, buat list dari 1 sampai lags
    if isinstance(lags, int):
        lags = list(range(1, lags + 1))

    for lag in lags:
        col_name = f"{target_col}_lag_{lag}"
        df[col_name] = df[target_col].shift(lag)
        print(f"✅ Lag feature dibuat: '{col_name}'")

    # Hapus baris dengan NaN akibat lag
    before = len(df)
    df = df.dropna()
    after = len(df)
    if before - after > 0:
        print(f"🗑️  {before - after} baris dihapus karena NaN dari lag features.")

    return df


def split_data(df, target_col, test_size=0.2):
    """
    Split data into training and testing sets.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe with features and target
    target_col : str
        Name of the target column
    test_size : float, optional (default=0.2)
        Proportion of data to use for testing (0.0 to 1.0)

    Returns:
    --------
    tuple
        (X_train, X_test, y_train, y_test)

    Notes:
    ------
    - Uses random_state=42 untuk reproducibility
    """
    if target_col not in df.columns:
        raise ValueError(f"Kolom target '{target_col}' tidak ditemukan!")

    # Pisahkan fitur (X) dan target (y)
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Hanya ambil kolom numerik untuk fitur
    X = X.select_dtypes(include=[np.number])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=42
    )

    print(f"✅ Data berhasil dibagi:")
    print(f"   → Training : {X_train.shape[0]} baris ({(1-test_size)*100:.0f}%)")
    print(f"   → Testing  : {X_test.shape[0]} baris ({test_size*100:.0f}%)")
    print(f"   → Fitur    : {list(X_train.columns)}")

    return X_train, X_test, y_train, y_test
