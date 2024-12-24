import os
import requests
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

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

    # Print the value counts of the 'Zip_loc' column in the training set as a dictionary
    print(X_train['Zip_loc'].value_counts().to_dict())
