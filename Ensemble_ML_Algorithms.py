import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score, make_scorer, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

random_state = np.random.RandomState(seed=29)
df = pd.read_csv('../data/music.csv')

le = LabelEncoder()
df['Class'] = le.fit_transform(df['Class'])

X = df.drop('Class', axis=1)
y = df['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=random_state)

sgd_params = {
    "clf__loss": ["log_loss", "huber"],
    "clf__penalty": ["l2", "l1"],
    "clf__alpha": [1e-4, 1e-3, 1e-2, 1e-1, ],
    "clf__learning_rate": ["constant", "adaptive"],
    "clf__eta0": [1e-4, 1e-3, 1e-2, 1e-1]
}

dt_params = {
    "clf__max_features": ["sqrt", "log2"],
    "clf__criterion": ["gini", "entropy", "log_loss"],
    'clf__max_depth': [None, 10, 20, 30],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 3, 4]
}

kn_params = {
    "clf__metric": ["minkowski", "cosine", "nan_euclidean", "manhattan"],
    "clf__n_neighbors": [2, 3, 4, 5, 6, 7, 8, 9],
    'clf__weights': ['uniform', 'distance'],
    'clf__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'clf__leaf_size': [30, 60],
    'clf__p': [1, 2],
}

sv_params = {
    "clf__kernel": ["poly", "sigmoid", "rbf"],
    "clf__C": [1e-4, 1e-2, 1.0, 1e2, 1e4],
    "clf__decision_function_shape": ["ovo", "ovr"],
    "clf__degree": [2, 3, 4],
    "clf__gamma": ['scale', 'auto'] + [0.1, 1.0, 10.0],
    "clf__coef0": [0.0, 1.0],
    "clf__shrinking": [True, False]
}

# Initialize classifiers
classifiers = {
    'sgd': SGDClassifier(random_state=random_state),
    'dt': DecisionTreeClassifier(random_state=random_state),
    'kn': KNeighborsClassifier(),
    'sv': SVC(random_state=random_state, probability=True)
}

all_results = []
# Evaluate both unoptimized and optimized models
for clf_name in classifiers:
    # Unoptimized model
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', classifiers[clf_name])])
    scores = cross_val_score(pipe, X_train, y_train, scoring='f1_macro', cv=5)
    all_results.append(pd.DataFrame({
        'model_type': clf_name,
        'params': 'default',
        'mean_test_score': np.mean(scores),
        'optimized': False
    }, index=['model_type', 'optimized']))

    # Optimized models
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', classifiers[clf_name])])
    grid = GridSearchCV(pipe, eval(f'{clf_name}_params'), scoring='f1_macro', n_jobs=-1)
    grid.fit(X_train, y_train)

    # Add all optimized candidates
    optimized_df = pd.DataFrame(grid.best_estimator_.named_steps['clf'].get_params(), index=[0])
    optimized_df['model_type'] = clf_name
    optimized_df['optimized'] = True
    all_results.append(optimized_df)

# Combine results and select best models
all_results = pd.concat(all_results, ignore_index=True)
all_results = all_results.sort_values('mean_test_score', ascending=False)

selected_models = all_results[all_results['mean_test_score'] > all_results['mean_test_score'].quantile(0.5)]
# Create voting classifier
voting_models = []
weights = []
for i, model in selected_models.iterrows():
    clf = classifiers[model['model_type']]
    if model['optimized']:
        params = {k.split('__')[1]: v for k, v in model['params'].items()}
        clf = clf.set_params(**params)

    # Ensure the classifier has predict_proba
    if not hasattr(clf, 'predict_proba'):
        clf = CalibratedClassifierCV(clf)

    pipeline = Pipeline([('scaler', StandardScaler()), ('clf', clf)])
    voting_models.append((f"{model['model_type']}_{'opt' if model['optimized'] else 'base'}_{i}", pipeline))
    weights.append(model['mean_test_score'])

# Normalize weights
weights = np.array(weights) / np.sum(weights)

# Build and evaluate ensemble
ensemble = VotingClassifier(
    estimators=voting_models,
    voting='soft',
    weights=weights,
    n_jobs=-1
)

ensemble.fit(X_train, y_train)
report = classification_report(y_test, ensemble.predict(X_test), output_dict=True)

print(report)
pd.DataFrame(report).to_csv('../data/stage4.csv')