import psycopg2
import json
import os
from util import establish_connection

conn = establish_connection()

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS companies;")
cursor.execute("CREATE TABLE companies (symbol VARCHAR(10) PRIMARY KEY, comp_name VARCHAR(100), lat FLOAT, lon FLOAT, country VARCHAR(100), geo_state VARCHAR(100));") 

with open('companies.csv', 'r',encoding='utf-8') as f:
    cursor.copy_expert("COPY companies FROM STDIN WITH (FORMAT CSV, HEADER 1)", f)
conn.commit()

#go through the folder stocks and make a table for each stock
for filename in os.listdir('stocks'):
    #asc.csv and true.csv escaped because psycopg2 sees them as keywords. We should probably find a better solution
    # See fx. this: https://stackoverflow.com/questions/43111996/why-postgresql-does-not-like-uppercase-table-names
    if filename.endswith(".csv") and filename != 'ASC.csv' and filename != 'TRUE.csv':
        symbol = filename.split('.')[0].lower()
        cursor.execute(f"DROP TABLE IF EXISTS {symbol};")
        #Volume should be type BIGINT but some volume values are apparently floats (.0)
        cursor.execute(f"CREATE TABLE {symbol} (date DATE PRIMARY KEY, open FLOAT, high FLOAT, low FLOAT, close FLOAT, adj_close FLOAT, volume FLOAT);")
        with open(f'stocks/{filename}', 'r',encoding='utf-8') as f:
            cursor.copy_expert(f"COPY {symbol} FROM STDIN WITH (FORMAT CSV, HEADER 1)", f)
        conn.commit()
