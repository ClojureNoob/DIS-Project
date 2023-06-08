from flask import Flask, render_template, send_file, request
import psycopg2
from util import establish_connection

app = Flask(__name__)

@app.route('/')
def render_map():
    conn = establish_connection()

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
    
    return render_template('content2.html',coordinates=coordinates, names=names)

if __name__ == '__main__':
    app.run()
