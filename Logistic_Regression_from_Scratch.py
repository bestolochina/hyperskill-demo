import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

# Create the CustomLogisticRegression class;
# Create the __init__ method;
# Create the sigmoid method;
# Create the predict_proba method;
class CustomLogisticRegression:
    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch

    def sigmoid(self, t):
        return 1 / (1 + np.exp(-t))

    def predict_proba(self, row, coef_):
        if self.fit_intercept:
            t = coef_[0] + np.dot(row, coef_[1:])
        else:
            t = np.dot(row, coef_)
        return self.sigmoid(t)

# Load the Breast Cancer Wisconsin dataset.
# Select worst concave points and worst perimeter as features and target as the target variable;
X, y = load_breast_cancer(return_X_y=True, as_frame=True)
X_selected = X[['worst concave points', 'worst perimeter']]

# Standardize X;
X_standardized = (X_selected - X_selected.mean()) / X_selected.std()

# Split the dataset including the target variable into training and test sets. Set train_size=0.8 and random_state=43;
X_train, X_test, y_train, y_test = train_test_split(X_standardized, y, train_size=0.8, random_state=43)

# Given the coefficients below, calculate the probabilities of the first 10 rows in the test set.
# You don't need the training set in this stage;
coefficients = [0.77001597, -2.12842434, -2.39305793]
clf = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=100)
probabilities = []
for row in range(10):
    row_values = X_test.iloc[row].values  # get the actual feature values as a NumPy array
    probabilities.append(clf.predict_proba(row=row_values, coef_=coefficients))
probabilities = [float(p) for p in probabilities]

# Print these probabilities as a Python list.
print(probabilities)
