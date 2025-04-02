import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
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

# 1.	Initialize the RandomForestClassifier with the random state and n_jobs.
clf = RandomForestClassifier(n_jobs=-1, random_state=random_state)

# 2.	Set up a Pipeline to preprocess with StandScaler before training with the classifier.
pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])

# 3.	Set param_grid parameter before tuning the model with GridSearchCV.
rf_params = {
    "clf__n_estimators": range(100, 500, 50),
    "clf__max_depth": range(1, 20, 1)
}

# 4.	Fit the model to the training set.
# grid = GridSearchCV(pipe, rf_params, scoring='f1_macro', n_jobs=-1)
grid = GridSearchCV(
    estimator=pipe,
    param_grid=rf_params,
    scoring='f1_macro',
    cv=5,
    n_jobs=-1,
    refit=True,
    return_train_score=False
)
grid.fit(X_train, y_train)

# 5.	Predict on the test set and evaluate using classification_report.
y_pred = grid.predict(X_test)

# 6.	Return the classification report as a dictionary by specifying output_dict as True.
report = classification_report(y_test, y_pred, output_dict=True)
print(report)

# 7.	Save the classification report as stage5.csv in the data directory.
pd.DataFrame(report).to_csv('../data/stage5.csv')
