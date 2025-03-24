import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score

random_state = np.random.RandomState(seed=29)

df = pd.read_csv(r'..\data\music.csv')
le = LabelEncoder()
X = df.drop(columns=['Class'])
y = le.fit_transform(df['Class'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=random_state)

classifiers = {'sgd': SGDClassifier(random_state=random_state),
               'dt': DecisionTreeClassifier(random_state=random_state),
               'kn': KNeighborsClassifier(),
               'sv': SVC(probability=True, random_state=random_state)}

results = {}
for clf_name, clf in classifiers.items():
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", clf)
      ])

    pipe.fit(X_train, y_train)

    y_train_pred = pipe.predict(X_train)
    y_test_pred = pipe.predict(X_test)

    train_f1 = round(f1_score(y_train, y_train_pred, average="macro", labels=[0, 1, 2, 3]), 3)
    test_f1 = round(f1_score(y_test, y_test_pred, average="macro", labels=[0, 1, 2, 3]), 3)

    results[clf_name] = {'f1_train': train_f1, 'f1_test': test_f1}

print(results)
