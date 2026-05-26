import pandas as pd
from sqlalchemy import create_engine

df = pd.read_excel('base.xlsx')
engine = create_engine('sqlite:///db.sqlite3')

df['occurrance'] = df['occurrance'].dt.strftime('%Y-%m-%d %H:%M')
df['date_ref'] = df['date_ref'].dt.strftime('%Y-%m-%d')

df.to_sql(
    name='reg_registry',
    con=engine,
    if_exists='append',
    index=False,
)