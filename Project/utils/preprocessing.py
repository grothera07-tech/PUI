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
    pass


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
    pass


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
    pass


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
    - Uses LabelEncoder for ordinal categorical features
    - Uses OneHotEncoder for nominal categorical features
    """
    pass


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
    - May also create: is_weekend, is_holiday (if applicable)
    """
    pass


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
    >>> df_with_lags
       sales  sales_lag_1  sales_lag_2
    0    100          NaN          NaN
    1    150        100.0          NaN
    2    200        150.0        100.0
    3    250        200.0        150.0
    """
    pass


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
    - Uses stratified split for classification tasks
    - Uses random_state=42 for reproducibility
    """
    pass
