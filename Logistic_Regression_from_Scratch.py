import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

class CustomLogisticRegression:
    def __init__(self, fit_intercept: bool = True, l_rate: float = 0.01, n_epoch: int = 100) -> None:
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.coef_: np.ndarray
        self.errors: list[list[float]] = []

    def sigmoid(self, t: float) -> float:
        return 1 / (1 + np.exp(-t))

    def predict_proba(self, row: np.ndarray, coef_: np.ndarray) -> float:
        t = np.dot(row, coef_)
        return self.sigmoid(t)

    def fit_mse(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        n_samples, n_weights = X_train.shape[0], X_train.shape[1] + 1 if self.fit_intercept else X_train.shape[1]
        self.coef_ = np.zeros(n_weights)

        for epoch in range(self.n_epoch):
            error_list = []
            for i, row in enumerate(X_train):
                x_i = np.insert(row, 0, 1) if self.fit_intercept else row
                y_hat = self.predict_proba(x_i, self.coef_)
                error = y_hat - y_train[i]
                gradient = error * y_hat * (1 - y_hat)

                self.coef_ -= (self.l_rate * gradient * x_i)

                error_list.append(float((error ** 2) / n_samples))
            self.errors.append(error_list)

    def fit_log_loss(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        n_samples, n_weights = X_train.shape[0], X_train.shape[1] + 1 if self.fit_intercept else X_train.shape[1]
        self.coef_ = np.zeros(n_weights)

        for epoch in range(self.n_epoch):
            error_list = []
            for i, row in enumerate(X_train):
                x_i = np.insert(row, 0, 1) if self.fit_intercept else row
                y_hat = self.predict_proba(x_i, self.coef_)
                error = y_hat - y_train[i]
                log_loss = -y_train[i] * np.log(y_hat + 1e-15) - (1 - y_train[i]) * np.log(1 - y_hat + 1e-15)

                self.coef_ -= (self.l_rate * error * x_i) / n_samples
                error_list.append(float(log_loss / n_samples))
            self.errors.append(error_list)

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

lr_log_loss = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
lr_log_loss.fit_log_loss(X_train, y_train)
y_hat = lr_log_loss.predict(X_test=X_test, cut_off=0.5)
accuracy_log_loss = accuracy_score(y_true=y_test, y_pred=y_hat)

lr_mse = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
lr_mse.fit_mse(X_train, y_train)
y_hat = lr_mse.predict(X_test=X_test, cut_off=0.5)
accuracy_mse = accuracy_score(y_true=y_test, y_pred=y_hat)

lr_sklearn = LogisticRegression()
lr_sklearn.fit(X_train, y_train)
y_hat = lr_sklearn.predict(X_test)
accuracy_sklearn = accuracy_score(y_true=y_test, y_pred=y_hat)

print({
    'mse_accuracy': accuracy_mse,
    'logloss_accuracy': accuracy_log_loss,
    'sklearn_accuracy': accuracy_sklearn,
    'mse_error_first': lr_mse.errors[0],
    'mse_error_last': lr_mse.errors[-1],
    'logloss_error_first': lr_log_loss.errors[0],
    'logloss_error_last': lr_log_loss.errors[-1]
})
print(f'''
Answers to the questions:
1) {min(lr_mse.errors[0]):.5f}
2) {min(lr_mse.errors[-1]):.5f}
3) {max(lr_log_loss.errors[0]):.5f}
4) {max(lr_log_loss.errors[-1]):.5f}
5) expanded
6) expanded
''')
# {'mse_accuracy': 0.8947368421052632, 'logloss_accuracy': 0.8947368421052632, 'sklearn_accuracy': 0.9035087719298246,
# 'mse_error_first': [0.0005494505494505495, 0.0005487619260382545, ...],
# 'mse_error_last': [0.0002595746966187235, 3.58874250533432e-05, ...],
# 'logloss_error_first': [0.0015234003968350445, 0.001523388285406441, ...],
# 'logloss_error_last': [0.0014739026005740753, 0.0014436401701211706, ...]}
# Answers to the questions:
# 1) 0.00005
# 2) 0.00000
# 3) 0.00153
# 4) 0.00580
# 5) expanded
# 6) expanded
