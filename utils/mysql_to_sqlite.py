from mysql.connector import connect
import sqlite3
import sys

conn_base = connect(host='127.0.0.1', username='iagoadm', password='IFe2026')
conn = sqlite3.connect('db.sqlite3')
cursor_base = conn_base.cursor()
cursor = conn.cursor()

TABLE = sys.argv[1]

cursor_base.execute(f'SHOW COLUMNS FROM financeiro.{TABLE}')
columns = [ f[0] for f in cursor_base.fetchall() ]

cursor_base.execute(f'SELECT * FROM financeiro.{TABLE}')
data = cursor_base.fetchall()

cmd = f'INSERT INTO {TABLE} (`{'`,`'.join(columns)}`) VALUES ({','.join('?'*len(columns))})'
print(cmd)
cursor.executemany(cmd, data)
conn.commit()