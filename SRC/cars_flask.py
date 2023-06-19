# Flask app to predict used car prices from used_cars.py

# import Flask and jsonify
from flask import Flask, request, jsonify, render_template

# import numpy
import numpy as np

# import pandas
import pandas as pd

# import Resource, Api and reqparser
from flask_restful import Api, Resource, reqparse

# import pickle
import pickle

app = Flask(__name__)
api = Api(app)

# load our pickled model
model = pickle.load(open('cars_model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template("Landing.html")

# @app.route('/predict')
# def cars():
#     return render_template("cars.html", prediction=0)

# json post route
@app.route('/predictcar', methods=['POST', 'GET'])
def predictLoan():
    # get data from post request
    # get data from html form
    data = request.form.to_dict()
    # data = request.get_json(force = True)
    if len(data) == 0:
        return render_template("cars.html", prediction= "Please enter valid data")
    
    elif len(data) !=0:

        # create a dataframe from our json data
        df = pd.DataFrame(data, index=[0])
        df['age'] = 2021 - int(df['year'])
        df.drop('year', axis=1, inplace=True)

        # predict loan status
        prediction = model.predict(df)

        # return prediction
        car_prediction = jsonify("Your predicted market value is USD :" + round(prediction[0], 0).astype(str) +\
                    " Happy Selling!!!")
        car_predict = round(prediction[0], 0)
        return render_template("cars.html", prediction=car_predict)



if __name__ == '__main__':
    app.run(debug=True, port=5000)