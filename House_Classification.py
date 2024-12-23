import os
import requests
import sys
import pandas as pd

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'house_class.csv' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/7vjkrlggmvr5bc1/house_class.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/house_class.csv', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('../Data/house_class.csv')

    print(df.shape[0])  # How many rows does the DataFrame have?
    print(df.shape[1])  # How many columns does the DataFrame have?
    print(df.isnull().any().any())  # Are there any missing values in the DataFrame (True or False)?
    print(df['Room'].max())  # What is the maximum number of rooms across the houses in the dataset?
    print(df.Area.mean().round(decimals=1))  # What is the mean area of the houses in the dataset?
    print(df['Zip_loc'].nunique())  # How many unique values does column Zip_loc contain?
