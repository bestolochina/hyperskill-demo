import os
import pandas as pd


def load_data() -> list[pd.DataFrame]:
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


def merge_data(dataframes_: list[pd.DataFrame]) -> pd.DataFrame:
    # Change the column names as in 'general.csv'
    dataframes_[1].columns = dataframes_[0].columns
    dataframes_[2].columns = dataframes_[0].columns

    # Merge the DataFrames into one
    result = pd.concat(dataframes_, ignore_index=True)

    # Delete the Unnamed: 0 column
    result = result.drop(columns=['Unnamed: 0'])

    # Return the result
    return result


if __name__ == '__main__':
    pd.set_option('display.max_columns', 8)

    # get a list of dataframes
    dataframes = load_data()

    # merge dataframes into one
    hospital_data = merge_data(dataframes)

    print(hospital_data.sample(n=20, random_state=30))
