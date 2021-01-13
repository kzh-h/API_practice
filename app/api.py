import sys
import pickle
import pandas as pd 

from datetime import datetime

from flask import Flask, request, jsonify, abort
from flask import render_template, redirect, url_for


# [TODO:] args?
VERSION = 'v0001'

sys.path.append('../src/models')
app = Flask(__name__)

preprocess = pickle.load(open(f'../models/{VERSION}/preprocess.pkl', 'rb'))
model = pickle.load(open(f'../models/{VERSION}/model.pkl', 'rb'))

@app.route('/api/predict', methods=["POST"])
def predict():
    """return prediction when POST request to /api/predict"""
    try:
        X = pd.DataFrame(request.json, index=[0])
        X["trade_date"] = datetime.now()
        # preprocess
        X = preprocess.transform(X)
        # predict
        y_pred = model.predict(X, num_iteration=model.best_iteration_)
        response = {
            'status': 'OK',
            'predicted': y_pred[0],
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        abort(400)


@app.errorhandler(400)
def error_handler(error):
    """abort(400) した時のレスポンス"""
    response = {"status": "Error", "message": "Invalid Parameters"}
    return jsonify(response), error.code


# access to index
@app.route('/')
def index():
    params = {
        'title': 'Welcome',
        'message': 'mlapp',
    }
    return render_template('app/index.html', params=params)


# access to post
@app.route('/post', methods=['GET', 'POST'])
def post():
    params = {
        'title': 'Welcome',
        'message': 'mlapp',
        'name': None,
    }
    if request.method == 'POST':
        params['name'] = request.form['name']
    return render_template('app/index.html', params=params)


if __name__ == "__main__":
    # app.run(debug=True)  # 開発用サーバーの起動
    app.run(host="0.0.0.0", debug=True)  # 開発用サーバーの起動
        