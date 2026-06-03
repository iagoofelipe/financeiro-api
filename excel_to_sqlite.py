import pandas as pd
from sqlalchemy import create_engine
import sys

engine = create_engine('sqlite:///db.sqlite3')

filename = '.temp/base.xlsx'
cols_to_cast = {
    'date': {'date_ref', 'closing_date', 'due_date'},
    'datetime': {'occurrance'},
}
all_sheets = '*' in sys.argv

for sheet_name in pd.ExcelFile(filename).sheet_names:
    if type(sheet_name) is not str:
        print('sheet_name must be a valid table string')
        continue

    if sheet_name not in sys.argv and not all_sheets:
        print(f'sheet "{sheet_name}" skipped')
        continue

    df = pd.read_excel(filename, sheet_name=sheet_name)
    df_cols = set(df.columns)

    for typeof, cols in cols_to_cast.items():
        for col in cols & df_cols:
            match typeof:
                case 'date': df[col] = df[col].dt.strftime('%Y-%m-%d')
                case 'date': df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M')

    match sheet_name:
        case 'reg_registry':
            df['occurrance'] = df['occurrance'].dt.strftime('%Y-%m-%d %H:%M')

    df.to_sql(
        name=sheet_name,
        con=engine,
        if_exists='append',
        index=False,
    )