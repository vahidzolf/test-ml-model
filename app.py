# Serve model as a flask application

import pickle
import numpy as np
from flask import Flask, request
import sqlite3



model = None
app = Flask(__name__)


def load_model():
    global model
    # model variable refers to the global variable
    with open('iris_trained_model.pkl', 'rb') as f:
        model = pickle.load(f)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())


@app.route('/')
def home_endpoint():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def get_prediction():
    # Works only for a single sample
    global id
    conn = sqlite3.connect('test.db')
    if request.method == 'POST':
        data = request.get_json()  # Get data posted as a json
        data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
        prediction = model.predict(data)  # runs globally loaded model on the data

        # write the request log into db
        insert_string = """INSERT INTO COMPANY
                          (id, headers, body )
                          VALUES (?, ?, ?);"""
        data_tuple = (int(id), str(request.headers), str(request.get_data()))
        cur = conn.cursor()
        cur.execute(insert_string, data_tuple)
        conn.commit()
        id += 1
    return str(prediction[0])


if __name__ == '__main__':
    load_model()  # load model at the beginning once only
    id = 1
    app.run(host='0.0.0.0', port=5000)