import pandas as pd


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
    def __init__(self, root: Node, min_samples: int=1) -> None:
        self.root = root
        self.min_samples = min_samples

    @staticmethod
    def _gini_impurity(labels: list) -> float:
        """Calculate Gini Impurity for one node"""
        if not labels:
            return 0.0  # empty list - perfect purity :)

        unique_labels = set(labels)
        probabilities = [labels.count(label) / len(labels) for label in unique_labels]
        gini_score = 1 - sum(p ** 2 for p in probabilities)

        return gini_score

    def _weighted_gini_impurity(self, labels1: list, labels2: list) -> float | None:
        """Calculate weighted Gini Impurity after splitting"""
        n1, n2 = len(labels1), len(labels2)
        total = n1 + n2

        if total == 0:
            return None  # If there are no samples, return None

        gini1 = self._gini_impurity(labels1)
        gini2 = self._gini_impurity(labels2)
        weighted_gini_score = (n1 / total) * gini1 + (n2 / total) * gini2

        return round(weighted_gini_score, 5)  # Round to 5 decimal places

    def _split_node(self, features: pd.DataFrame, target: pd.Series) -> tuple[float, str, int, pd.Index, pd.Index]:
        """Find the best split by minimizing weighted Gini Impurity.
        Take the dataset and the target variable as the arguments and return the minimum of the weighted Gini Impurity
        for the current node, the chosen feature, its chosen value, a list of the left node indexes, and a list of the
        right node indexes."""
        best_gini = float('inf')
        best_feature = None
        best_value = None
        best_left_indexes = None
        best_right_indexes = None

        for feature in features.columns:
            unique_values = features[feature].unique()
            for value in unique_values:
                left_indexes = features.index[features[feature] == value]
                right_indexes = features.index[features[feature] != value]

                left_labels = target.loc[left_indexes].tolist()
                right_labels = target.loc[right_indexes].tolist()

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
                or self._gini_impurity(target.tolist()) == 0  # All targets are the same (pure node)
                or (features.nunique(axis=0) == 1).all()  # All features have the same value across all rows
        ):
            node.set_term(target.value_counts().idxmax())  # Assign the most common label
            return

        # If the node is not a leaf, call the splitting function
        best_gini, best_feature, best_value, best_left_indexes, best_right_indexes = self._split_node(features, target)

        # print the details of the splitting
        print(f'Made split: {best_feature} is {best_value}')

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
    
    def fit(self, features: pd.DataFrame, target: pd.Series) -> None:
        """Trains the model based on features and target"""
        self._recursive_splitting(self.root, features, target)


if __name__ == '__main__':
    # Stage 4
    path = input()  # r'test/data_stage4.csv'
    df = pd.read_csv(path, index_col=0)
    features = df.drop(columns=['Survived'])
    target = df.Survived
    root = Node()
    tree = DecisionTree(root)
    tree.fit(features, target)
