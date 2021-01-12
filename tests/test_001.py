import requests
import json
import pytest

def test_normal_input():
    URL = "http://localhost:5000/api/predict"
    DATA = {
        "address": "東京都千代田区",
        "area": 30,
        "building_year": 2013,
    }

    response = requests.post(URL, json=DATA)
    print(response.txt)
    result = json.loads(response.text)
    assert response.status_code == 200
    assert result['status'] == 'OK'
    assert 0 <= result['predicted']
