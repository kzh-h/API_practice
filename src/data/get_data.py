'''
    get data from website.
    Caution: In container, this module raise an error
'''

import requests
import json
import pandas as pd
import os

url = "https://www.land.mlit.go.jp/webland/api/TradeListSearch"
# 東京都，2005Q3 ~ 2019Q3のデータ（DLに10分ほどかかるので注意）
payload = {"area": 13, "from": 20053, "to": 20193}
response = requests.get(url, params=payload)

data = json.loads(response.text)
df = pd.DataFrame(data["data"])

# 保存
os.makedirs("../../data/raw", exist_ok=True)
df.to_csv("../../data/raw/raw.csv", index=False)