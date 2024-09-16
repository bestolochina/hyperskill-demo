import sqlite3
import pandas as pd
import numpy as np
import re
from pathlib import Path
import json


class Convoy:
    def __init__(self) -> None:
        self.dispatch: dict[str, callable] = {
            'to_json': self.s3db_to_json,
            'to_s3db': self.checked_to_s3db,
            'to_checked': self.csv_to_checked,
            'to_csv': self.xlsx_to_csv
        }
        self.file_name: str = ''

    def start(self) -> None:
        while True:
            self.file_name = input('Input file name\n').strip().lower()
            if Path(self.file_name).suffix in {'.csv', '.xlsx', '.s3db'}:
                break

        if self.file_name.endswith('.s3db'):
            operation = 'to_json'
        elif self.file_name.endswith('[checked].csv'):
            operation = 'to_s3db'
        elif self.file_name.endswith('csv'):
            operation = 'to_checked'
        else:
            operation = 'to_csv'

        self.process_data(operation)

    def process_data(self, operation_type):
        if operation_type in self.dispatch:
            return self.dispatch[operation_type]()
        else:
            return "Invalid input type"

    def xlsx_to_csv(self, xlsx_file: str = None) -> None:
        if xlsx_file is None:
            xlsx_file = self.file_name

        sheet_name: str = 'Vehicles'
        df: pd.DataFrame = pd.read_excel(xlsx_file, sheet_name=sheet_name, dtype=str)
        csv_file: str = xlsx_file[:-4] + 'csv'
        df.to_csv(path_or_buf=csv_file, index=False, header=True)
        lines_num: int = df.shape[0]
        report: str = ('1 line was' if lines_num == 1 else f'{lines_num} lines were') + f' added to {csv_file}'
        print(report)
        return self.csv_to_checked(csv_file)

    def csv_to_checked(self, csv_file: str = None) -> None:
        if csv_file is None:
            csv_file = self.file_name

        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_file, header='infer')
        checked_csv_file: str = csv_file[:-4] + '[CHECKED].csv'

        counter: int = 0
        pattern: str = r'\D*(\d*).*'
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                data = df.iloc[row, column]
                re_match = re.match(pattern=pattern, string=data)
                if re_match:
                    fixed_data = re_match.group(1)
                    if data != fixed_data:
                        counter += 1
                        df.iloc[row, column] = fixed_data
                else:
                    df.iloc[row, column] = np.nan

        df.to_csv(path_or_buf=checked_csv_file, index=False, header=True)
        report: str = ('1 cell was' if counter == 1 else f'{counter} cells were') + f' corrected in {checked_csv_file}'
        print(report)
        return self.checked_to_s3db(checked_csv_file)

    def checked_to_s3db(self, checked_csv_file: str = None) -> None:
        if checked_csv_file is None:
            checked_csv_file = self.file_name

        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=checked_csv_file, header='infer')
        db_file: str = checked_csv_file[:-13] + '.s3db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        columns = df.columns.tolist()
        table_name = 'convoy'
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns[0]} INTEGER PRIMARY KEY, " + ", ".join(
            [f"{col} INTEGER NOT NULL" for col in columns[1:]]) + ");"
        cursor.execute(create_table_query)
        # result = df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        insert_query: str = f'INSERT or REPLACE INTO {table_name} VALUES (?, ?, ?, ?)'
        cursor.executemany(insert_query, df.values.tolist())
        result = cursor.rowcount

        conn.commit()
        conn.close()

        report: str = ('1 record was' if result == 1 else f'{result} records were') + f' inserted into {db_file}'
        print(report)
        return self.s3db_to_json(db_file)

    def s3db_to_json(self, db_file: str = None) -> None:
        if db_file is None:
            db_file = self.file_name

        # Connect to the SQLite database
        table_name: str = 'convoy'
        json_file: str = db_file[:-4] + 'json'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Fetch all rows from the table
        select_query: str = f'SELECT * FROM {table_name}'
        cursor.execute(select_query)
        rows = cursor.fetchall()
        count = len(rows)

        # Fetch column names
        column_names = [description[0] for description in cursor.description]

        # Convert the rows into a list of dictionaries (JSON format)
        data = [dict(zip(column_names, row)) for row in rows]
        my_dict = {table_name: data}

        # Write to a JSON file
        with open(json_file, 'w') as file:
            json.dump(my_dict, file, indent=4)

        conn.close()

        report: str = ('1 vehicle was' if count == 1 else f'{count} vehicles were') + f' saved into {json_file}'
        print(report)
        # print(my_dict)


def main():
    convoy = Convoy()
    convoy.start()


if __name__ == '__main__':
    main()
