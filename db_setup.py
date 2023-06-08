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

cursor.execute("DROP TABLE IF EXISTS prices;")
cursor.execute("CREATE TABLE prices (symbol VARCHAR(10), date DATE, price FLOAT);")

with open('prices.csv', 'r',encoding='utf-8') as f:
    cursor.copy_expert("COPY prices FROM STDIN WITH (FORMAT CSV, HEADER 1)", f)