import pandas as pd


def gini_impurity(labels: list) -> float:
    """Calculate Gini Impurity for one node"""
    if not labels:
        return 0.0  # Instead of None, return 0.0 for an empty node (perfect purity)

    unique_labels = set(labels)
    probabilities = [labels.count(label) / len(labels) for label in unique_labels]
    gini_score = 1 - sum(p ** 2 for p in probabilities)

    return gini_score


def weighted_gini_impurity(labels1: list, labels2: list) -> float | None:
    """Calculate weighted Gini Impurity after splitting"""
    n1, n2 = len(labels1), len(labels2)
    total = n1 + n2

    if total == 0:
        return None  # If there are no samples, return None

    gini1 = gini_impurity(labels1)
    gini2 = gini_impurity(labels2)
    weighted_gini_score = (n1 / total) * gini1 + (n2 / total) * gini2

    return round(weighted_gini_score, 5)  # Round to 5 decimal places


def split_node(features: pd.DataFrame, target: pd.Series) -> tuple[float, str, int, list[int], list[int]] :
    """take the dataset and the target variable as the arguments and return the minimum of the weighted Gini Impurity
    for the current node, the chosen feature, its chosen value, a list of the left node indexes, and a list of the
    right node indexes"""
    best_gini = float('inf')
    best_feature = None
    best_value = None
    best_left_indexes = None
    best_right_indexes = None

    for feature in features.columns:
        unique_values = features[feature].unique()
        for value in unique_values:
            left_indexes = features.index[features[feature] == value].tolist()
            right_indexes = features.index[features[feature] != value].tolist()

            left_labels = target.loc[left_indexes].tolist()
            right_labels = target.loc[right_indexes].tolist()

            gini = weighted_gini_impurity(left_labels, right_labels)

            if gini < best_gini:
                best_gini = gini
                best_feature = feature
                best_value = value
                best_left_indexes = left_indexes
                best_right_indexes = right_indexes

    return best_gini, best_feature, best_value, best_left_indexes, best_right_indexes


def stage_2():
    """Split function"""
    path = input()  # r'test/data_stage2.csv'
    df = pd.read_csv(path, index_col=0)
    features = df.drop(columns=['Survived'])
    target = df.Survived

    print(*split_node(features, target))


if __name__ == '__main__':
    stage_2()
