import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import matplotlib.pyplot as plt

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
    indexes = np.random.choice(a=len(x_data), size=len(x_data), replace=True)
    x_sample = x_data[indexes]
    y_sample = y_data[indexes]
    return x_sample, y_sample


def stage_2(x_data, y_data):
    print(create_bootstrap(x_data, y_data)[1].tolist()[:10])


def stage_3(X_train, X_val, y_train, y_val):
    # Use the first tree of the forest to make predictions on the test set.
    # Calculate the accuracy of the test set using the predictions.
    # Print the resulting accuracy rounded to three digits after the dot (for example, 3.141).
    my_forest = RandomForestClassifier()
    my_forest.fit(X_train, y_train)
    y_predict = my_forest.forest[0].predict(X_val)
    accuracy = accuracy_score(y_true=y_val, y_pred=y_predict)
    print(round(accuracy, 3))


def stage_4(X_train, X_val, y_train, y_val):
    # Fit the model on the whole training set using the parameters from the previous stage;
    # Predict labels for the first ten objects in the test set and print the result.
    my_forest = RandomForestClassifier()
    my_forest.fit(X_train, y_train)
    predictions = my_forest.predict(X_val)
    print(predictions.tolist()[:10])


def stage_5(X_train, X_val, y_train, y_val):
    # Fit your RandomForestClassifier on the whole training set;
    # Predict labels for all the objects in the test set.
    # Calculate and print the resulting accuracy rounded to three digits after the dot (for example, 3.141).
    my_forest = RandomForestClassifier()
    my_forest.fit(X_train, y_train)
    predictions = my_forest.predict(X_val)
    accuracy = accuracy_score(y_true=y_val, y_pred=predictions)
    print(round(accuracy, 3))


def stage_6(X_train, X_val, y_train, y_val):
    # Fit your RandomForestClassifier on the whole train set using n_trees ranging from 1 to 600 with a step of 1.
    # For each classifier, calculate the resulting accuracy on the test set.
    # Print the first 20 of the resulting accuracy values rounded to three digits after the dot (for example, 3.141);
    #
    # Plot the resulting dependence of accuracy from the number of trees.
    # Do you have the expected behavior of your model? This objective is optional, and it won't be part of the test.
    accuracies = []
    results = []
    for n_trees in range(1, 21):
        my_forest = RandomForestClassifier(n_trees=n_trees)
        my_forest.fit(X_train, y_train)
        predictions = my_forest.predict(X_val)
        accuracy = round(accuracy_score(y_true=y_val, y_pred=predictions), 3)
        accuracies.append(accuracy)
        results.append({'n_trees': n_trees, 'accuracy': accuracy})
    print(accuracies)

    # # Convert results to a DataFrame
    # results_df = pd.DataFrame(results)
    #
    # # Plot using Matplotlib
    # plt.figure(figsize=(15, 9))
    # plt.plot('n_trees', 'accuracy', data=results_df, marker='o', linestyle='-', color='b', label='Validation Accuracy')
    # plt.title('Accuracy vs. Number of Trees', fontsize=16)
    # plt.xlabel('Number of Trees', fontsize=14)
    # plt.ylabel('Accuracy', fontsize=14)
    # plt.grid(True)
    #
    # # Update x-ticks
    # plt.xticks(np.arange(0, 601, 50))  # Set x-ticks from 0 to 600 with steps of 50
    #
    # plt.legend(fontsize=12)
    # plt.show()


class RandomForestClassifier():
    def __init__(self, n_trees=10, max_depth=np.iinfo(np.int64).max, min_error=1e-6):

        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_error = min_error

        self.forest: list[DecisionTreeClassifier] = []
        self.is_fit = False

    def fit(self, X_train, y_train):
        for _ in tqdm(range(self.n_trees)):
            X_sample, y_sample = create_bootstrap(X_train, y_train)
            tree = DecisionTreeClassifier(max_depth=self.max_depth,
                                          max_features='sqrt',
                                          min_impurity_decrease=self.min_error)
            tree.fit(X_sample, y_sample)
            self.forest.append(tree)

        self.is_fit = True

    def predict(self, X_test):
        if not self.is_fit:
            raise AttributeError('The forest is not fit yet! Consider calling .fit() method.')

        # Collect predictions from all trees
        all_predictions = np.array([tree.predict(X_test) for tree in self.forest])  # Shape: (n_trees, n_samples)

        # Aggregate predictions per sample using majority voting
        final_predictions = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=all_predictions)

        return final_predictions


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

    stage_6(X_train, X_val, y_train, y_val)
