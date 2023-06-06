from flask import Flask, render_template, send_file, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def render_map():
    '''
    conn = psycopg2.connect(
    host="your_host",
    port="your_port",
    database="your_database",
    user="your_username",
    password="your_password"
    )

    cursor = conn.cursor()

    query = "SELECT lat, lon FROM companies;"
    cursor.execute(query)

    # Fetch all the rows and store the coordinates
    coordinates = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
    '''
    #test coordinates with a list of tuples (lat, lon)
    coordinates = [(40.7128, -74.0060), (48.8566, 2.3522), (51.5074, -0.1278)]
    names = ['New York', 'Paris', 'London']
    prices = [100,200, 300]
    return render_template('content.html',coordinates=coordinates, names=names, prices=prices)

if __name__ == '__main__':
    app.run()
