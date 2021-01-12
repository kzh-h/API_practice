import sys
import pickle
import pandas as pd 

from datetime import datetime

from flask import Flask, request, jsonify, abort


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


if __name__ == "__main__":
    app.run(debug=True)  # 開発用サーバーの起動
        