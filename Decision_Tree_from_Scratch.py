import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


class Node:

    def __init__(self):
        # class initialization
        self.left = None
        self.right = None
        self.term = False
        self.label = None
        self.feature = None
        self.value = None

    def set_split(self, feature, value):
        # this function saves the node splitting feature and its value
        self.feature = feature
        self.value = value

    def set_term(self, label):
        # if the node is a leaf, this function saves its label
        self.term = True
        self.label = label


class DecisionTree:
    def __init__(self, root: Node, num_features: list[str], min_samples: int = 1) -> None:
        self.root = root
        self.num_features = num_features
        self.min_samples = min_samples

    @staticmethod
    def _gini_impurity(labels: pd.Series) -> float:
        """Calculate Gini Impurity for one node"""
        if labels.empty:
            return 0.0  # empty list - perfect purity :)

        probabilities = labels.value_counts(normalize=True).values
        gini_score = 1 - sum(p ** 2 for p in probabilities)

        return gini_score

    def _weighted_gini_impurity(self, labels1: pd.Series, labels2: pd.Series) -> float | None:
        """Calculate weighted Gini Impurity after splitting"""
        n1, n2 = len(labels1), len(labels2)
        total = n1 + n2

        if total == 0:
            return None  # If there are no samples, return None

        gini1 = self._gini_impurity(labels1)
        gini2 = self._gini_impurity(labels2)
        weighted_gini_score = (n1 / total) * gini1 + (n2 / total) * gini2

        return round(weighted_gini_score, 5)  # Round to 5 decimal places

    def _split_node(self, features: pd.DataFrame, target: pd.Series)\
            -> tuple[float, str, int | float, pd.Index, pd.Index]:
        """Find the best split by minimizing weighted Gini Impurity"""
        best_gini = float("inf")
        best_feature = None
        best_value = None
        best_left_indexes = None
        best_right_indexes = None

        for feature in features.columns:
            unique_values = features[feature].unique()

            for value in unique_values:
                if feature in self.num_features:  # numerical values
                    left_indexes = features.loc[features[feature] <= value].index
                else:  # categorical values
                    left_indexes = features.loc[features[feature] == value].index

                right_indexes = features.index.difference(left_indexes)

                left_labels = target.loc[left_indexes]
                right_labels = target.loc[right_indexes]

                gini = self._weighted_gini_impurity(left_labels, right_labels)

                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_value = value
                    best_left_indexes = left_indexes
                    best_right_indexes = right_indexes

        return best_gini, best_feature, best_value, best_left_indexes, best_right_indexes

    def _recursive_splitting(self, node: Node, features: pd.DataFrame, target: pd.Series) -> None:
        """Recursive splitting"""
        # check whether the current node is a leaf
        if (
                features.shape[0] <= self.min_samples  # Only one sample remains
                or self._gini_impurity(target) == 0  # All targets are the same (pure node)
                or (features.nunique(axis=0) == 1).all()  # All features have the same value across all rows
        ):
            node.set_term(target.value_counts().idxmax())  # Assign the most common label
            return

        # If the node is not a leaf, call the splitting function
        best_gini, best_feature, best_value, best_left_indexes, best_right_indexes = self._split_node(features, target)

        # store the chosen feature and its threshold value
        node.set_split(best_feature, best_value)

        # Create left and right child nodes
        node.left = Node()
        node.right = Node()

        # Extract the subset of features and target for the left and right nodes
        left_features = features.loc[best_left_indexes].reset_index(drop=True)
        left_target = target.loc[best_left_indexes].reset_index(drop=True)

        right_features = features.loc[best_right_indexes].reset_index(drop=True)
        right_target = target.loc[best_right_indexes].reset_index(drop=True)

        # Recursively split the left and right nodes
        self._recursive_splitting(node.left, left_features, left_target)
        self._recursive_splitting(node.right, right_features, right_target)

    def _recursive_predicting(self, node: Node, row: pd.Series) -> str:
        """Takes the current node and the current sample (one row) and returns a predicted label for the given sample"""
        if node.term:
            return node.label

        if ((node.feature in self.num_features and row[node.feature] <= node.value) or  # numerical value
                (node.feature not in self.num_features and row[node.feature] == node.value)):  # categorical value
            return self._recursive_predicting(node.left, row)
        else:
            return self._recursive_predicting(node.right, row)

    def fit(self, features: pd.DataFrame, target: pd.Series) -> None:
        """Trains the model based on features and target"""
        self._recursive_splitting(self.root, features, target)

    def predict(self, features: pd.DataFrame) -> pd.Series:
        """Takes a set of new observations and return an array with predictions of a target variable"""
        return features.apply(lambda row: self._recursive_predicting(self.root, row), axis=1)


def stage_9():
    train_set, test_set = input().split()
    # train_set, test_set = r'test/data_stage9_train.csv', r'test/data_stage9_test.csv'
    df_train, df_test = pd.read_csv(train_set, index_col=0), pd.read_csv(test_set, index_col=0)
    features_train, target_train = df_train.drop(columns=['Survived']), df_train.Survived
    features_test, target_test = df_test.drop(columns=['Survived']), df_test.Survived
    root_ = Node()
    tree = DecisionTree(root=root_, num_features=["Age", "Fare"], min_samples=74)
    tree.fit(features_train, target_train)
    target_predicted = tree.predict(features_test)
    conf_matrix = confusion_matrix(target_test, target_predicted, normalize='true')
    tp, tn = conf_matrix[1, 1], conf_matrix[0, 0]
    print(round(tp, 3), round(tn, 3))


if __name__ == '__main__':
    stage_9()
