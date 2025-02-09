import os
import requests

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape


def stage_1(df: pd.DataFrame) -> None:
    """Perform linear regression on rating vs salary."""
    # Make X a DataFrame with a predictor rating and y a series with a target salary;
    X, y = df[['rating']], df['salary']  # X as DataFrame (2D), y as Series (1D)

    # Split predictor and target into training and test sets. Use test_size=0.3 and random_state=100 parameters;
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    # Fit the linear regression model with the following formula on the training data: salary ∼ rating
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict a salary with the fitted model on test data and calculate the MAPE;
    y_hat = model.predict(X_test)
    model_mape = round(mape(y_true=y_test, y_pred=y_hat), 5)

    # Print three float numbers: the model intercept, the slope, and the MAPE
    # rounded to five decimal places and separated by whitespace.
    intercept = round(model.intercept_, 5)
    slope = round(model.coef_[0], 5)
    print(intercept, slope, model_mape)


def stage_2(df: pd.DataFrame) -> None:
    """Linear regression with predictor transformation."""
    # Make X a DataFrame with a predictor rating and y a series with a target salary;
    X, y = df[['rating']], df['salary']  # X as DataFrame (2D), y as Series (1D)

    mapes = []
    for power in (2, 3, 4):
        # X_p = X.apply(lambda col: col**power)
        # X_p = X.pow(power)
        X_p = X ** power  # Raise predictor to the power of 2, 3, 4.

        # Split the predictors and target into training and test sets. Use test_size=0.3 and random_state=100 parameters
        X_train, X_test, y_train, y_test = train_test_split(X_p, y, test_size=0.3, random_state=100)

        # Fit the linear model of salary on rating, make predictions and calculate the MAPE;
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_hat = model.predict(X_test)
        mapes.append(round(mape(y_true=y_test, y_pred=y_hat), 5))

    # Print the best MAPE obtained by fitting and running the models described above.
    # The MAPE is a float number rounded to five decimal places.
    print(min(mapes))


def stage_3(df: pd.DataFrame) -> None:
    """Linear regression with many independent variables"""
    # Make X a DataFrame with predictors and y a series with a target.
    X = df.drop(columns='salary')
    y = df['salary']

    # Split the predictors and target into training and test sets. Use test_size=0.3 and random_state=100.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    # Fit the model predicting salary based on all other variables.
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Print the model coefficients separated by a comma.
    print(*model.coef_, sep=', ')


if __name__ == '__main__':
    # checking ../Data directory presence
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # download data if it is unavailable
    if 'data.csv' not in os.listdir('../Data'):
        url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/data.csv', 'wb').write(r.content)

    # read data
    data = pd.read_csv('../Data/data.csv')
    # print(data)

    stage_3(data)
