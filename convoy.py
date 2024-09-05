import pandas as pd

xlsx_file = input('Input file name\n').strip()
sheet_name = 'Vehicles'
csv_name = xlsx_file[:-4] + 'csv'

my_df = pd.read_excel(xlsx_file, sheet_name=sheet_name, dtype=str)
lines_num = my_df.shape[0]
report = ('1 line was' if lines_num == 1 else f'{lines_num} lines were') + f' imported to {csv_name}'

my_df.to_csv(path_or_buf=csv_name, index=False, header=True)

print(report)
