import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from typing import Union

class CustomLogisticRegression:
    def __init__(self, fit_intercept: bool = True, l_rate: float = 0.01, n_epoch: int = 100) -> None:
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.coef_: np.ndarray

    def sigmoid(self, t: float) -> float:
        return 1 / (1 + np.exp(-t))

    def predict_proba(self, row: np.ndarray, coef_: np.ndarray) -> float:
        t = np.dot(row, coef_)
        return self.sigmoid(t)

    def fit_mse(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        n_weights = X_train.shape[1] + 1 if self.fit_intercept else X_train.shape[1]
        self.coef_ = np.zeros(n_weights)

        for _ in range(self.n_epoch):
            for i, row in enumerate(X_train):
                x_i = np.insert(row, 0, 1) if self.fit_intercept else row
                y_hat = self.predict_proba(x_i, self.coef_)
                error = (y_hat - y_train[i]) * y_hat * (1 - y_hat)
                self.coef_ -= self.l_rate * error * x_i

    def predict(self, X_test: np.ndarray, cut_off: float = 0.5) -> np.ndarray:
        predictions: list[int] = []
        for row in X_test:
            if self.fit_intercept:
                row = np.insert(row, 0, 1)
            y_hat = self.predict_proba(row, self.coef_)
            predictions.append(1 if y_hat >= cut_off else 0)
        return np.array(predictions)

X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_selected = X[['worst concave points', 'worst perimeter', 'worst radius']]

X_standardized = (X_selected - X_selected.mean()) / X_selected.std()

X_train, X_test, y_train, y_test = train_test_split(X_standardized, y, train_size=0.8, random_state=43)
X_train = X_train.values
X_test = X_test.values
y_train = y_train.values
y_test = y_test.values

lr = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
lr.fit_mse(X_train, y_train)
y_hat = lr.predict(X_test=X_test, cut_off=0.5)
accuracy = accuracy_score(y_true=y_test, y_pred=y_hat)

print({
    'coef_': lr.coef_.tolist(),
    'accuracy': round(accuracy, 2)
})
