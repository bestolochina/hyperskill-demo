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

# scroll down to the bottom to implement your solution

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

    print(list(A_office_data_df.index))
    print(list(B_office_data_df.index))
    print(list(hr_data_df.index))
