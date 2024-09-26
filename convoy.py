import sqlite3
import pandas as pd
import numpy as np
import re
from pathlib import Path
import json
from lxml import etree


class Convoy:
    def __init__(self) -> None:
        self.dispatch: dict[str, callable] = {
            'to_json_xml': self.s3db_to_json_xml,
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
            operation = 'to_json_xml'
        elif self.file_name.endswith('[checked].csv'):
            operation = 'to_s3db'
        elif self.file_name.endswith('csv'):
            operation = 'to_checked'
        else:
            operation = 'to_csv'

        self.process_data(operation)

    def process_data(self, operation):
        if operation in self.dispatch:
            return self.dispatch[operation](self.file_name)
        else:
            return "Invalid input type"

    def xlsx_to_csv(self, xlsx_file: str) -> None:
        df: pd.DataFrame = pd.read_excel(xlsx_file, sheet_name='Vehicles', dtype=str)
        csv_file: str = xlsx_file[:-4] + 'csv'
        df.to_csv(path_or_buf=csv_file, index=False, header=True)
        lines_num: int = df.shape[0]
        print(('1 line was' if lines_num == 1 else f'{lines_num} lines were') + f' added to {csv_file}')
        return self.csv_to_checked(csv_file)

    def csv_to_checked(self, csv_file: str) -> None:
        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=csv_file, header='infer')
        checked_csv_file: str = csv_file[:-4] + '[CHECKED].csv'

        counter: int = 0
        for row in range(df.shape[0]):
            for column in range(df.shape[1]):
                data = df.iloc[row, column]
                re_match = re.match(pattern=r'\D*(\d*).*', string=data)
                if re_match:
                    fixed_data = re_match.group(1)
                    if data != fixed_data:
                        counter += 1
                        df.iloc[row, column] = fixed_data
                else:
                    df.iloc[row, column] = np.nan

        df.to_csv(path_or_buf=checked_csv_file, index=False, header=True)
        print(('1 cell was' if counter == 1 else f'{counter} cells were') + f' corrected in {checked_csv_file}')
        return self.checked_to_s3db(checked_csv_file)

    def checked_to_s3db(self, checked_csv_file: str) -> None:
        df: pd.DataFrame = pd.read_csv(filepath_or_buffer=checked_csv_file, header='infer')
        df = self.add_score(df)

        db_file: str = checked_csv_file[:-13] + '.s3db'
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        columns = df.columns.tolist()
        create_table_query = f"CREATE TABLE IF NOT EXISTS convoy ({columns[0]} INTEGER PRIMARY KEY, " + ", ".join(
            [f"{col} INTEGER NOT NULL" for col in columns[1:]]) + ");"
        cursor.execute(create_table_query)
        insert_query: str = f'INSERT or REPLACE INTO convoy VALUES (?, ?, ?, ?, ?)'
        cursor.executemany(insert_query, df.values.tolist())
        result = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        print(('1 record was' if result == 1 else f'{result} records were') + f' inserted into {db_file}')
        return self.s3db_to_json_xml(db_file, df)

    @staticmethod
    def add_score(df: pd.DataFrame) -> pd.DataFrame:

        def calculate_score(row) -> int:
            score: int = 0
            pitstops_num: float = (row['fuel_consumption'] * 450 / 100) / row['engine_capacity']
            score += 0 if pitstops_num >= 2 else 1 if pitstops_num >= 1 else 2  # score for number of pitstops
            fuel_burned: float = 450 / row['fuel_consumption']
            score += 2 if fuel_burned <= 230 else 1  # score for fuel consumption
            score += 2 if row['maximum_load'] >= 20 else 0  # score for capacity
            return score

        # Apply function to each row and create a new column
        df['score'] = df.apply(calculate_score, axis=1)
        return df

    def s3db_to_json_xml(self, db_file: str, df: pd.DataFrame) -> None:
        json_file: str = db_file[:-4] + 'json'
        xml_file: str = db_file[:-4] + 'xml'

        # Convert DataFrame to dict
        convoy_list = df.to_dict(orient='records')
        list_for_json = []
        list_for_xml = []

        for entry in convoy_list:  # Separate entries for JSON and XML
            if entry['score'] > 3:
                list_for_json.append(entry)
            else:
                list_for_xml.append(entry)

        for entry in list_for_json:  # Remove score
            del entry['score']
        for entry in list_for_xml:
            del entry['score']
        rows_json = len(list_for_json)
        rows_xml = len(list_for_xml)
        dict_for_json = {'convoy': list_for_json}
        dict_for_xml = {'convoy': list_for_xml}

        with open(json_file, 'w') as file:
            json.dump(dict_for_json, file, indent=4)

        if rows_xml != 0:
            # Create the root element
            root = etree.Element("convoy")
            # Create XML tree from dictionary
            for vehicle in dict_for_xml['convoy']:
                vehicle_elem = etree.SubElement(root, "vehicle")
                for key, value in vehicle.items():
                    child = etree.SubElement(vehicle_elem, key)
                    child.text = str(value)

            # Convert the XML tree to a byte string (pretty print for readability)
            xml_data = etree.tostring(root, pretty_print=True, encoding='utf-8')
            # Write the XML to a file
            with open(xml_file, 'wb') as file:  # "wb" mode for writing bytes
                file.write(xml_data)
        else:
            with open(xml_file, 'w') as file:
                file.write('<convoy></convoy>')

        report: str = ('1 vehicle was' if rows_json == 1 else f'{rows_json} vehicles were') + f' saved into {json_file}'
        print(report)
        report: str = ('1 vehicle was' if rows_xml == 1 else f'{rows_xml} vehicles were') + f' saved into {xml_file}'
        print(report)


def main():
    convoy = Convoy()
    convoy.start()


if __name__ == '__main__':
    main()
