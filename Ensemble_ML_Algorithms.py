import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, f1_score

random_state = np.random.RandomState(seed=29)

df = pd.read_csv(r'..\data\music.csv')
le = LabelEncoder()
X = df.drop(columns=['Class'])
y = le.fit_transform(df['Class'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=random_state)

classifiers = {
    'sgd': {'clf': SGDClassifier(random_state=random_state),
            'params': {"clf__loss": ["log_loss", "huber"],
                       "clf__penalty": ["l2", "l1"],
                       "clf__alpha": [1e-4, 1e-3, 1e-2, 1e-1],
                       "clf__learning_rate": ["constant", "adaptive"],
                       "clf__eta0": [1e-4, 1e-3, 1e-2, 1e-1]}},

    'dt': {'clf': DecisionTreeClassifier(random_state=random_state),
           'params': {"clf__max_features": ["sqrt", "log2"],
                      "clf__criterion": ["gini", "entropy", "log_loss"],
                      "clf__max_depth": [None, 10, 20, 30],
                      "clf__min_samples_split": [2, 5, 10],
                      "clf__min_samples_leaf": [1, 2, 3, 4]}},

    'kn': {'clf': KNeighborsClassifier(),
           'params': {"clf__metric": ["minkowski", "cosine", "nan_euclidean", "manhattan"],
                      "clf__n_neighbors": [2, 3, 4, 5, 6, 7, 8, 9],
                      "clf__weights": ['uniform', 'distance'],
                      "clf__algorithm": ['auto', 'ball_tree', 'kd_tree', 'brute'],
                      "clf__leaf_size": [30, 60],
                      "clf__p": [1, 2]}},

    'sv': {'clf': SVC(probability=True, random_state=random_state),
           'params': {"clf__kernel": ["poly", "sigmoid", "rbf"],
                      "clf__C": [1e-4, 1e-2, 1.0, 1e2, 1e4],
                      "clf__decision_function_shape": ["ovo", "ovr"],
                      "clf__degree": [2, 3, 4],
                      "clf__gamma": ['scale', 'auto', 0.1, 1.0, 10.0],
                      "clf__coef0": [0.0, 1.0],
                      "clf__shrinking": [True, False]}}
}

# Define scoring metric
f1 = make_scorer(f1_score, average="macro", labels=[0, 1, 2, 3])

results = {}

for clf_name, clf_dict in classifiers.items():
    clf = clf_dict['clf']
    params = clf_dict['params']

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", clf)
    ])

    # GridSearchCV with cross-validation
    grid_search = GridSearchCV(pipe, params, cv=5, scoring=f1, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Use the best estimator
    best_model = grid_search.best_estimator_

    # Predict on train and test sets
    y_train_pred = best_model.predict(X_train)
    y_test_pred = best_model.predict(X_test)

    # Compute F1 scores
    train_f1 = round(f1_score(y_train, y_train_pred, average="macro", labels=[0, 1, 2, 3]), 3)
    test_f1 = round(f1_score(y_test, y_test_pred, average="macro", labels=[0, 1, 2, 3]), 3)

    # Store results
    results[clf_name] = {'f1_train': train_f1, 'f1_test': test_f1}

# Save results to CSV
df_results = pd.DataFrame.from_dict(results)
df_results.to_csv(r'..\data\stage3.csv')
