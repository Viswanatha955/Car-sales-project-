import pickle
from flask import Flask
print(dir(Flask))
from flask import Flask, render_template, request, app, jsonify, url_for
import numpy
import pandas as pd
from sklearn.preprocessing import LabelEncoder


app = Flask(__name__)

car = pd.read_csv('full data.csv')
print(car)

## load the model
model = pickle.load(open(r'C:\Carsales\Second-hand-car-price-prediction\dt_model.pkl','rb'))
label_encoder = LabelEncoder()


@app.route("/")
@app.route("/home")
def predict_page():
    brands = sorted(car['Brand'].unique())
    names = sorted(car['Name'].unique())
    year = sorted(car['Year'].unique(), reverse=True)
    Mode = sorted(car['Model'].unique())
    gear = car['Transmission'].unique()
    Fuel_type = car['Fuel Type'].unique()
    state = car['State'].unique()
    return render_template('index.html', brands=brand,names=name,years=year,Model= Mode, Gear = gear, Fuel_type=Fuel_type,state=state)


def home_page():
    return render_template('home.html')

@app.route("/Predict")



@app.route("/market")
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
        {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
        {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    ]
    return render_template('market.html', items=items)


@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.json['data']
    print(data)
    data = pd.DataFrame(data, index=['1'])
    for i in data.columns:
        if data[i].dtype == object:
            data[i] = label_encoder.fit_transform(data[i])


    output = model.predict(data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['post'])
def predict():
    data = [request.form.values()]
    print("this is my first frame:", data)
    data = pd.DataFrame(data, index=['1'])
    print("Second frame",data)
    for i in data.columns:
        if data[i].dtype == object:
            data[i] = label_encoder.fit_transform(data[i])
    print("Third frame",data)
    output = model.predict(data)[0]
    print("output is",output)
    return render_template('home.html', prediction_text = "predicted car price is ${}".format(output))


if __name__=="__main__":
    app.run(debug=True)
