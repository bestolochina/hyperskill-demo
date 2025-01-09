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


def output_statistics(df: pd.DataFrame) -> None:
    # Which hospital has the highest number of patients?

    # method 1
    hospital_counts = df['hospital'].value_counts()
    max_hospital = hospital_counts.index[0]  # hospital has the highest number of patients
    max_count = hospital_counts.iloc[0]  # the number of patients in the hospital

    # method 2
    # hospital_counts = df['hospital'].groupby(by=df['hospital']).agg(func='count').sort_values(ascending=False)
    # max_hospital = hospital_counts.idxmax()
    # max_count = hospital_counts.max()
    print(f'The answer to the 1st question is {max_hospital}')

    # What share of the patients in the general hospital suffers from stomach-related issues?
    # Round the result to the third decimal place.

    # method 1
    # general = df.loc[(df['hospital'] == 'general')]
    # general_stomach = general.loc[(general['diagnosis'] == 'stomach')]
    # general_stomach_share = round(general_stomach.shape[0] / general.shape[0], 3)

    # method 2
    # general_stomach_share = round(
    #     len(df[(df['hospital'] == 'general') & (df['diagnosis'] == 'stomach')]) /
    #     len(df[df['hospital'] == 'general']),
    #     3)

    # method 3
    general_stomach_share = round(
        len(df.query("hospital == 'general' and diagnosis == 'stomach'")) /
        len(df.query("hospital == 'general'")),
        3)
    print(f'The answer to the 2nd question is {general_stomach_share}')

    # What share of the patients in the sports hospital suffers from dislocation-related issues?
    # Round the result to the third decimal place.
    sports_dislocation_share = round(
        len(df[(df['hospital'] == 'sports') & (df['diagnosis'] == 'dislocation')]) /
        len(df[df['hospital'] == 'sports']),
        3)
    print(f'The answer to the 3rd question is {sports_dislocation_share}')

    # What is the difference in the median ages of the patients in the general and sports hospitals?
    general_median = df.loc[(df['hospital'] == 'general'), 'age'].median()
    sports_median = df.loc[(df['hospital'] == 'sports'), 'age'].median()
    difference = general_median - sports_median  # not sure whether should I round up the result or not
    print(f'The answer to the 4th question is {difference}')

    # After data processing at the previous stages, the blood_test column has three values: t = a blood test was
    # taken, f = a blood test wasn't taken, and 0 = there is no information. In which hospital the blood test was
    # taken the most often (there is the biggest number of t in the blood_test column among all the hospitals)? How
    # many blood tests were taken?

    blood_test_counts = df.loc[(df['blood_test'] == 't'), 'blood_test'].groupby(by=df['hospital']).agg(func='count')
    max_blood_tests_hospital = blood_test_counts.idxmax()
    max_blood_tests_count = blood_test_counts.max()

    print(f'The answer to the 5th question is {max_blood_tests_hospital}, {max_blood_tests_count} blood tests')


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
    output_statistics(hospital_data)
