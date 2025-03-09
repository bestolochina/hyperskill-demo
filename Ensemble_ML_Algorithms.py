import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

random_state = np.random.RandomState(seed=29)

df = pd.read_csv(r'..\data\music.csv')
le = LabelEncoder()
X = df.drop(columns=['Class'])
y = le.fit_transform(df['Class'])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=random_state)

print({"train": [X_train.shape, y_train.shape], "test": [X_test.shape, y_test.shape]})
