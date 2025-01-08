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


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Delete all the empty rows
    df = df.dropna(axis=0, how='all').copy()  # Use `.copy()` to avoid potential view-related issues

    # Correct all the gender column values to 'f' and 'm'
    df.loc[:, 'gender'] = df['gender'].map({'male': 'm', 'man': 'm', 'female': 'f', 'woman': 'f'})

    # Replace NaN values in the gender column for 'prenatal' hospital with 'f'
    df.loc[(df['hospital'] == 'prenatal') & (df['gender'].isna()), 'gender'] = 'f'

    # Replace NaN values in other specified columns with 0
    columns_to_fill = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
    df.loc[:, columns_to_fill] = df[columns_to_fill].fillna(value=0)

    return df


def output_data(df: pd.DataFrame) -> None:
    # Print shape of the resulting DataFrame like in example "Data shape: (442, 14)"
    print(f'Data shape: {df.shape}')

    # Print random 20 rows of the resulting DataFrame. For the reproducible output set random_state=30
    # Tip: To complete the last step use pandas.DataFrame.sample(n=20, random_state=30).
    print(df.sample(n=20, random_state=30))


if __name__ == '__main__':
    # Keep pd.set_option('display.max_columns', 8) in your code.
    pd.set_option('display.max_columns', 8)

    # get a list of dataframes
    dataframes = load_data()

    # merge dataframes into one
    hospital_data = merge_data(dataframes)

    # preprocess data
    hospital_data = preprocess_data(hospital_data)

    # output data
    output_data(hospital_data)
