import sys
import os
import pickle
import json
import argparse
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

import lightgbm as lgb

from pipeline import Date2Int, ToCategorical, PcaFeature



parser = argparse.ArgumentParser(
    description='Paramete of lightGBM'
)
parser.add_argument('--input-file', type=argparse.FileType("r"), default="default.json")
parser.add_argument('--version', type=str, default='v000')
args = parser.parse_args()
params = json.load(args.input_file)
VERSION = args.version

# データ読み込み
print('\nload preprocessed_data...')
df = pd.read_csv("../../data/interim/preprocessed_data.csv")
y = df["price"]
X = df.drop("price", axis=1)

# 前処理パイプラインの定義
# execute pca.fit in advance
pca_1_cols = ['area', 'building_year'] 
pca_1 = PCA(n_components=1)
pca_1.fit(X[pca_1_cols])
preprocess = Pipeline(steps=[
    ("date_to_int", Date2Int(target_col="trade_date")),
    ("to_category", ToCategorical(target_col="address")),
    ("pca_feats", PcaFeature(cols=pca_1_cols, pca=pca_1, n_components=1)),
])

# 前処理
X = preprocess.transform(X)

# データを分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 学習
# params = {
#     "n_estimators": 100_000,
#     "min_child_samples": 15,
#     "max_depth": 4,
#     "colsample_bytree": 0.7,
#     "random_state": 42
# }
print('\ntrain...')
model = lgb.LGBMRegressor(**params)
model.fit(
    X_train, y_train,
    eval_metric="rmse",
    eval_set=[(X_test, y_test)],
    early_stopping_rounds=100,
)
print("\nbest scores:", dict(model.best_score_["valid_0"]))

# 保存
os.makedirs(f'../../models/{VERSION}/', exist_ok=True)
pickle.dump(pca_1, open(f"../../models/{VERSION}/pca_1.pkl", "wb"))
pickle.dump(preprocess, open(f"../../models/{VERSION}/preprocess.pkl", "wb"))
pickle.dump(model, open(f"../../models/{VERSION}/model.pkl", "wb"))
os.makedirs(f'../../config/{VERSION}/', exist_ok=True)
with open(f'../../config/{VERSION}/params.json', mode="w") as f:
    json.dump(params, f, indent=4)
print('Done\n')