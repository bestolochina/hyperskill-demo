import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

np.random.seed(52)


def convert_embarked(x):
    if x == 'S':
        return 0
    elif x == 'C':
        return 1
    else:
        return 2


def stage_1(X_train, X_test, y_train, y_test) -> None:
    # Use the sklearn's DecisionTreeClassifier to create a decision tree.
    clf = DecisionTreeClassifier()

    # Fit the model to the train set and make a prediction for the test set.
    clf.fit(X_train, y_train)
    y_predict = clf.predict(X_test)

    # Print accuracy of the predictions rounded to three digits after the dot (for example, 3.141).
    # Use sklearn's accuracy_score function.
    print(round(accuracy_score(y_true=y_test, y_pred=y_predict), 3))


def create_bootstrap(x_data, y_data):
    # take the features and the target values as parameters and return a bootstrap sample
    mask = np.random.choice(a=len(x_data), size=len(x_data), replace=True)
    x_sample = x_data[mask]
    y_sample = y_data[mask]
    return x_sample, y_sample


if __name__ == '__main__':
    data = pd.read_csv('https://www.dropbox.com/s/4vu5j6ahk2j3ypk/titanic_train.csv?dl=1')

    data.drop(
        ['PassengerId', 'Name', 'Ticket', 'Cabin'],
        axis=1,
        inplace=True
    )
    data.dropna(inplace=True)

    # Separate these back
    y = data['Survived'].astype(int)
    X = data.drop('Survived', axis=1)

    X['Sex'] = X['Sex'].apply(lambda x: 0 if x == 'male' else 1)
    X['Embarked'] = X['Embarked'].apply(lambda x: convert_embarked(x))

    X_train, X_val, y_train, y_val = train_test_split(X.values, y.values, stratify=y, train_size=0.8)

    X_sample, y_sample = create_bootstrap(X_train, y_train)
    sample = y_sample.tolist()[:10]
    print(sample)
