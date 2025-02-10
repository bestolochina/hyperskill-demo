import os
import requests
from itertools import combinations
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


def stage_4(df: pd.DataFrame) -> None:
    """Test for multicollinearity and variable selection.

    The function calculates the correlation matrix for numeric predictors,
    identifies variables with a correlation (with any other variable) greater
    than 0.2, and then tests linear models by removing either one or two of these
    variables. It prints the lowest MAPE (rounded to five decimal places) among these models.
    """
    # Calculate the correlation matrix for the numeric variables;
    # Make X, a DataFrame with all the predictor variables, and y, a series with the target.
    X, y = df.drop(columns='salary'), df['salary']
    corr_matrix = X.corr()

    # Find the variables where the correlation coefficient is greater than 0.2.
    high_corr_labels = set()
    for label in corr_matrix.index:
        # Drop self-correlation (always 1)
        row = corr_matrix.loc[label].drop(label)
        # Check if any correlation exceeds the threshold
        if (row > 0.2).any():
            high_corr_labels.add(label)
    comb1 = list(combinations(high_corr_labels, 1))
    comb2 = list(combinations(high_corr_labels, 2))
    all_combinations = comb1 + comb2

    # Split the predictors and the target into training and test sets. Use test_size=0.3 and random_state=100.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    # Fit the linear models for salary prediction based on the subsets of other variables. The subsets are as follows:
    # First, try to remove each of the three variables you've found in step 4.
    # Second, remove each possible pair of these three variables.
    # Make predictions and print the lowest MAPE. The MAPE is a floating number rounded to five decimal places.
    mapes = []
    for comb in all_combinations:
        cols_to_drop = list(comb)  # because initially it's a tuple and we need a list
        model = LinearRegression()
        x_train = X_train.drop(columns=cols_to_drop)
        model.fit(x_train, y_train)
        x_test = X_test.drop(columns=cols_to_drop)
        y_hat = model.predict(x_test)
        mapes.append(round(mape(y_true=y_test, y_pred=y_hat), 5))
    print(min(mapes))


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

    stage_4(data)
