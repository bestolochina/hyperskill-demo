import os
import requests
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from category_encoders import TargetEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


def one_hot_encoding(X_train_, X_test_, y_train_, y_test_):
    # Create the encoder and specify the drop='first' parameter to drop the first column, created by the encoder
    encoder = OneHotEncoder(drop='first')

    # Fit the encoder to the training data using three categorical columns: Zip_area, Zip_loc, Room
    encoder.fit(X_train_[['Zip_area', 'Zip_loc', 'Room']])

    # Transform the training and the test datasets with the fitted encoder
    X_train_transformed = pd.DataFrame(encoder.transform(X_train_[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
                                       index=X_train_.index)
    X_test_transformed = pd.DataFrame(encoder.transform(X_test_[['Zip_area', 'Zip_loc', 'Room']]).toarray(),
                                      index=X_test_.index)

    # Return the transformed data to the dataset
    X_train_final = X_train_[['Area', 'Lon', 'Lat']].join(X_train_transformed)
    X_test_final = X_test_[['Area', 'Lon', 'Lat']].join(X_test_transformed)

    # Convert column names to strings
    X_train_final.columns = X_train_final.columns.astype(str)
    X_test_final.columns = X_test_final.columns.astype(str)

    # Predict the target values
    y_predict_ = prediction(X_train_final, X_test_final, y_train_)
    report = classification_report(y_test_, y_predict_, output_dict=True)
    print(f'OneHotEncoder:{report['macro avg']['f1-score']:.2f}')


def ordinal_encoding(X_train_, X_test_, y_train_, y_test_):
    # Create the encoder
    encoder = OrdinalEncoder()

    # Fit the encoder to the training data
    encoder.fit(X_train_[['Zip_area', 'Zip_loc', 'Room']])

    # Transform the training and test datasets
    X_train_transformed = pd.DataFrame(encoder.transform(X_train_[['Zip_area', 'Zip_loc', 'Room']]),
                                       index=X_train_.index,
                                       columns=['Zip_area', 'Zip_loc', 'Room'])
    X_test_transformed = pd.DataFrame(encoder.transform(X_test_[['Zip_area', 'Zip_loc', 'Room']]),
                                      index=X_test_.index,
                                      columns=['Zip_area', 'Zip_loc', 'Room'])

    # Replace the original categorical columns with the transformed ones
    X_train_final = X_train_.drop(['Zip_area', 'Zip_loc', 'Room'], axis=1).join(X_train_transformed)
    X_test_final = X_test_.drop(['Zip_area', 'Zip_loc', 'Room'], axis=1).join(X_test_transformed)

    # Predict the target values
    y_predict_ = prediction(X_train_final, X_test_final, y_train_)
    report = classification_report(y_test_, y_predict_, output_dict=True)
    print(f'OrdinalEncoder:{report['macro avg']['f1-score']:.2f}')


def target_encoding(X_train_, X_test_, y_train_, y_test_):
    # Create the encoder
    encoder = TargetEncoder(cols=['Zip_area', 'Room', 'Zip_loc'])

    # Fit the encoder on training data
    encoder.fit(X_train_[['Zip_area', 'Zip_loc', 'Room']], y_train)

    # Transform only the specified columns
    X_train_transformed = encoder.transform(X_train_[['Zip_area', 'Zip_loc', 'Room']])
    X_test_transformed = encoder.transform(X_test_[['Zip_area', 'Zip_loc', 'Room']])

    # Replace the original categorical columns with the transformed ones
    X_train_final = X_train_[['Area', 'Lon', 'Lat']].join(X_train_transformed[['Room', 'Zip_area', 'Zip_loc']])
    X_test_final = X_test_[['Area', 'Lon', 'Lat']].join(X_test_transformed[['Room', 'Zip_area', 'Zip_loc']])

    # Predict the target values
    y_predict_ = prediction(X_train_final, X_test_final, y_train_)
    report = classification_report(y_test_, y_predict_, output_dict=True)
    print(f'TargetEncoder:{report['macro avg']['f1-score']:.2f}')


def prediction(X_train_final_, X_test_final_, y_train_):
    # Use DecisionTreeClassifier from scikit-learn.
    # Fit the model to the training data and predict the house prices on the test data
    clf = DecisionTreeClassifier(criterion='entropy',
                                 max_features=3,
                                 splitter='best',
                                 max_depth=6,
                                 min_samples_split=4,
                                 random_state=3)
    clf.fit(X_train_final_, y_train_)
    y_predict_ = clf.predict(X_test_final_)
    return y_predict_


if __name__ == '__main__':
    # Define the data directory and file paths
    data_dir = os.path.join('..', 'Data')
    csv_path = os.path.join(data_dir, 'house_class.csv')

    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    # Download data if it is unavailable
    if 'house_class.csv' not in os.listdir(data_dir):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/7vjkrlggmvr5bc1/house_class.csv?dl=1"
        try:
            r = requests.get(url, allow_redirects=True)
            with open(csv_path, 'wb') as f:
                f.write(r.content)
            sys.stderr.write("[INFO] Loaded.\n")
        except requests.RequestException as e:
            sys.stderr.write(f"[ERROR] Failed to download the dataset: {e}\n")
            sys.exit(1)

    # Set display options to show all columns
    pd.set_option('display.max_columns', None)

    # Load the dataset into a DataFrame
    df = pd.read_csv(csv_path)

    # Create two separate datasets for features (X) and target (y)
    X, y = df.loc[:, ['Area', 'Room', 'Lon', 'Lat', 'Zip_area', 'Zip_loc']], df['Price']

    # Split the dataset into training and testing sets with stratification
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.3,
                                                        stratify=X['Zip_loc'].values,
                                                        random_state=1)

    one_hot_encoding(X_train, X_test, y_train, y_test)
    ordinal_encoding(X_train, X_test, y_train, y_test)
    target_encoding(X_train, X_test, y_train, y_test)
