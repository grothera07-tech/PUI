from flask import Flask, render_template, request
from model import train_model
import pandas as pd

app = Flask(__name__)

model = train_model()

# load data buat grafik
data = pd.read_csv('data.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    harga = float(request.form['harga'])
    promosi = int(request.form['promosi'])
    
    prediction = model.predict([[harga, promosi]])
    
    # ambil data lama
    labels = list(range(1, len(data)+1))
    values = data['penjualan'].tolist()
    
    # tambahin hasil prediksi ke grafik
    values.append(round(prediction[0], 2))
    labels.append("Prediksi")
    
    return render_template('index.html',
                           hasil=round(prediction[0], 2),
                           labels=labels,
                           values=values)

if __name__ == '__main__':
    app.run(debug=True)