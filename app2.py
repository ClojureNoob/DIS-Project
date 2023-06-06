from flask import Flask, render_template, send_file, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def render_map():
    with open('pw.config', 'r') as f:
        pw = f.read().strip()

    conn = psycopg2.connect(
        host="localhost",	
        port="5432",
        database="nasdaq",
        user="postgres",
        password= pw,
        options="-c client_encoding=utf8" 
    )

    cursor = conn.cursor()

    query = "SELECT lat, lon FROM companies;"
    cursor.execute(query)
    coordinates = cursor.fetchall()

    query = "SELECT comp_name FROM companies;"
    cursor.execute(query)
    names = cursor.fetchall()

    query = "SELECT symbol FROM companies;"
    cursor.execute(query)
    symbols = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return render_template('content.html',coordinates=coordinates, names=names, prices=prices)

if __name__ == '__main__':
    app.run()
