from flask import Flask, render_template, send_file, request
from us_states import states
from countries import country_list
import psycopg2

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_connection_string'
#db = SQLAlchemy(app)



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
    prices = [(100),(200), (300)]
    return render_template('content.html',coordinates=coordinates, names=names, prices=prices)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Keeps track os states, and update their status whether they have been chosen by the user.
    """
    us_states = [
        states
    ]

    if request.method == 'POST':
        chosen_state = request.form.get('state')
        for state in us_states:
            if state['name'] == chosen_state:
                state['chosen'] = True
            else:
                state['chosen'] = False

    return render_template('index.html', us_states=us_states)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Keeps track of countries, and update their status whether they have been chosen by the user.
    """
    countries = [
        country_list
    ]

    if request.method == 'POST':
        chosen_country = request.form.get('country')
        for country in countries:
            if country['name'] == chosen_country:
                country['chosen'] = True
            else:
                country['chosen'] = False

    return render_template('index.html', countries=countries)

def chosen_states():
    chosen_states = [state['name'] for state in states if state['chosen']]
    return chosen_states

def chosen_countries():
    chosen_countries = [country['name'] for country in country_list if country['chosen']]
    return chosen_countries

def query_countries_states():
    countries = chosen_countries()
    states = chosen_states()

    conn = psycopg2.connect(
        host = "",
        port = "",
        database = "",
        user = "",
        password = ""
    )

    cursor = conn.cursor()



    query = f"Select "

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

if __name__ == '__main__':
    app.run()
