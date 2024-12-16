import pandas as pd
import logging
import requests
import os


# Configure logging with a format that includes the logger name
logging.basicConfig( filename='HR_Data_Analysis.log',
                     encoding='utf-8',
                     level=logging.DEBUG,
                     format='%(name)s - %(levelname)s - %(message)s')

# Create and configure loggers
app_logger = logging.getLogger('app')
# db_logger = logging.getLogger('app.database')
# auth_logger = logging.getLogger('app.authentication')


def count_bigger_5(series: pd.Series) -> int:
    return (series > 5).sum()


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # Read XML data into DataFrames
    A_office_data_df = pd.read_xml('../Data/A_office_data.xml')
    B_office_data_df = pd.read_xml('../Data/B_office_data.xml')
    hr_data_df = pd.read_xml('../Data/hr_data.xml')

    # # Check for null values in each column
    # print(A_office_data_df.isnull().values.any())  # Returns True if any null values exist
    # print(B_office_data_df.isnull().values.any())
    # print(hr_data_df.isnull().values.any())

    new_a_index = [f'A{row}' for row in A_office_data_df['employee_office_id']]
    A_office_data_df.index = new_a_index
    new_b_index = [f'B{row}' for row in B_office_data_df.employee_office_id]
    B_office_data_df.index = new_b_index
    new_hr_index = [row for row in hr_data_df['employee_id']]
    hr_data_df.index = new_hr_index

    # Concatenating A_office_data_df and B_office_data_df dataframes
    AB_office_data_df = pd.concat([A_office_data_df, B_office_data_df])

    # Merging hr_data_df and AB_office_data_df
    result_df = pd.merge(AB_office_data_df, hr_data_df,
                         how='left',
                         left_index=True,
                         right_index=True,
                         indicator=True)

    # Filter rows where the indicator column shows data in both datasets
    result_df = result_df[result_df['_merge'] == 'both']

    # Drop 3 columns - 'employee_office_id', 'employee_id', '_merge'
    result_df = result_df.drop(columns=['employee_office_id', 'employee_id', '_merge'])

    # Sort result_df by index
    result_df = result_df.sort_index(axis=0, inplace=False)

    # Aggregation
    result = result_df.groupby('left').agg({
        'number_project': ['median', count_bigger_5],
        'time_spend_company': ['mean', 'median'],
        'Work_accident': 'mean',
        'last_evaluation': ['mean', 'std']
    }).round(2).to_dict()

    print(result)
