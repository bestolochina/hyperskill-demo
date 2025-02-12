import pandas as pd
import logging
import requests
import os


# Configure logging with a format that includes the logger name
# logging.basicConfig( filename='HR_Data_Analysis.log',
#                      encoding='utf-8',
#                      level=logging.DEBUG,
#                      format='%(name)s - %(levelname)s - %(message)s')
# Create and configure loggers
# app_logger = logging.getLogger('app')
# db_logger = logging.getLogger('app.database')
# auth_logger = logging.getLogger('app.authentication')


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

    new_a_index = [f'A{row}' for row in A_office_data_df['employee_office_id']]
    A_office_data_df.index = new_a_index
    new_b_index = [f'B{row}' for row in B_office_data_df.employee_office_id]
    B_office_data_df.index = new_b_index
    new_hr_index = [row for row in hr_data_df['employee_id']]
    hr_data_df.index = new_hr_index

    # Concatenating A_office_data_df and B_office_data_df dataframes
    AB_office_data_df = pd.concat([A_office_data_df, B_office_data_df])

    # Merging hr_data_df and AB_office_data_df
    df = pd.merge(AB_office_data_df, hr_data_df,
                  how='left',
                  left_index=True,
                  right_index=True,
                  indicator=True)

    # Filter rows where the indicator column shows data in both datasets
    df = df[df['_merge'] == 'both']

    # Drop 3 columns - 'employee_office_id', 'employee_id', '_merge'
    df = df.drop(columns=['employee_office_id', 'employee_id', '_merge'])

    # Sort result_df by index
    df = df.sort_index(axis=0, inplace=False)

    # Use df.pivot_table() to generate the first pivot table: Department as index, left and salary as columns,
    # average_monthly_hours as values. Output median values in the table.
    table1 = df.pivot_table(index='Department',
                            columns=['left', 'salary'],
                            values='average_monthly_hours',
                            aggfunc='median')
    # For the currently employed: the median value of the working hours of high-salary employees is smaller
    # than the hours of the medium-salary employees,
    # OR: For the employees who left: the median value of working hours of low-salary employees is smaller
    # than the hours of high-salary employees
    table1 = table1.loc[
        (table1[(1, 'high')] < table1[(1, 'medium')]) | (table1[(0, 'low')] < table1[(0, 'high')])
    ].round(2)
    # print(table1)
    print(table1.to_dict())

    # Use df.pivot_table() to generate the second pivot table: time_spend_company as index, promotion_last_5years as
    # column, satisfaction_level and last_evaluation as values. Output the min, max, and mean values in the table.
    table2 = df.pivot_table(index='time_spend_company',
                            columns='promotion_last_5years',
                            values=['satisfaction_level', 'last_evaluation'],
                            aggfunc=['min', 'max', 'mean'])
    # Filter the table by the following rule: select only those rows where the previous mean evaluation score is
    # higher for those without promotion than those who had
    table2 = table2.loc[
        table2[('mean', 'last_evaluation', 0)] > table2[('mean', 'last_evaluation', 1)]
    ].round(2)
    # print(table2)
    print(table2.to_dict())
