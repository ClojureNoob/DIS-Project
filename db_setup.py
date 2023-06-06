import psycopg2

#There may be a better way to do this
with open('config.config', 'r') as f:
    config = json.load(f)

db_name = config['db_name']
db_user = config['db_user']
pw = config['pw']
host = config['host']
port = config['port']

conn = psycopg2.connect(
    host=host,	
    port=port,
    database= db_name,
    user=db_user,
    password= pw,
    options="-c client_encoding=utf8" 
    )

cursor = conn.cursor()

#We should either implement a cascade or have mulitiple DROP TABLE statements here
cursor.execute("DROP TABLE IF EXISTS companies;")

#Order of columns might be incorrect here
cursor.execute("CREATE TABLE companies (symbol VARCHAR(10) PRIMARY KEY, comp_name VARCHAR(100), lat FLOAT, lon FLOAT, country VARCHAR(100), geo_state VARCHAR 100);") 

#BE AWARE: currently missing a copy of both the companies and the prices tables. 
cursor.execute("COPY companies FROM 'companies.csv' DELIMITER ',' CSV HEADER;")