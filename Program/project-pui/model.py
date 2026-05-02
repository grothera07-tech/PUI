import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_model():
    data = pd.read_csv('data.csv')
    
    X = data[['harga', 'promosi']]
    y = data['penjualan']
    
    model = RandomForestRegressor()
    model.fit(X, y)
    
    return model