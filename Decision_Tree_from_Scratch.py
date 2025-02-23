def gini_impurity(labels: list) -> float | None:
    """Calculate Gini Impurity for one node"""
    if not labels:
        return None  # If there are no samples, return None

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


if __name__ == '__main__':
    arr1, arr2, arr3 = [[int(n) for n in input().split()] for _ in range(3)]
    print(round(gini_impurity(arr1), 2), round(weighted_gini_impurity(arr2, arr3), 2))
