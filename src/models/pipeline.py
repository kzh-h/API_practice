import os
import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA


class skPlumberBase(BaseEstimator, TransformerMixin):
    """Pipelineに入れられるTransformerのベース"""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return self


class Date2Int(skPlumberBase):

    def __init__(self, target_col):
        self.target_col = target_col

    def transform(self, X):
        """unix時間に変換する"""
        dates = pd.to_datetime(X[self.target_col]).astype(np.int64) / 10**9
        X[self.target_col] = dates.astype(int)
        return X


class ToCategorical(skPlumberBase):
    """LightGBMにcategoryだと認識させるため，
    カテゴリカル変数をpandas category型にする
    """

    def __init__(self, target_col):
        self.target_col = target_col

    def transform(self, X):
        X[self.target_col] = X[self.target_col].astype("category")
        return X


class PcaFeature(skPlumberBase):
    """
        PCA特徴量の作成
    """

    def __init__(self, cols, pca, n_components):
        self.cols = cols
        self.pca = pca
        self.n_components = n_components

    def transform(self, X):
        pca_feats = pd.DataFrame(
            self.pca.transform(X[self.cols]),
            columns=[f'{"_".join(self.cols)}_pca_{i}' \
                for i in range(1, self.n_components+1)]
        )
        X = pd.concat([X, pca_feats], axis=1)

        return X
        
