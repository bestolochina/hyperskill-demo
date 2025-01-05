import os
import pandas as pd


def load_data():
    # define the data directory and file names
    data_dir = 'test'
    files = ['general.csv', 'prenatal.csv', 'sports.csv']

    # load the datasets into DataFrame
    dataframes_ = []
    for file in files:
        csv_path = os.path.join(data_dir, file)
        dataframes_.append(pd.read_csv(csv_path))

    # return the list of DataFrames
    return dataframes_


if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)

    # get a list of dataframes
    dataframes = load_data()

    for df in dataframes:
        print(df.head(n=20))
