from flask import Flask, render_template, send_file, request
from us_states import states
from countries import country_list
import psycopg2
from util import establish_connection

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_connection_string'
#db = SQLAlchemy(app)



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
    
    return render_template('test.html',coordinates=coordinates, names=names)

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

def create_portfolio_table(portfolio):
    conn = establish_connection()
    cursor = conn.cursor()

    for row in portfolio:
        symbol = row[0]
        cursor.execute(f"SELECT date, close FROM {symbol};")
        stock_data = cursor.fetchall()

        table_name = f"portfolio_{symbol}"
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(f"CREATE TABLE {table_name} (date DATE, close FLOAT, symbol VARCHAT(10))")

        for stock_row in stock_data:
            date = stock_row[0]
            close = stock_row[4]
            cursor.execute(f"INSERT INTO {table_name} (data, close, symbol) VALUES (%s, %s, %s);", (date, close, symbol))

        conn.commit()

    cursor.close()
    conn.close()

    

def chosen_states():
    chosen_states = [state['name'] for state in states if state['chosen']]
    return chosen_states

def chosen_countries():
    chosen_countries = [country['name'] for country in country_list if country['chosen']]
    return chosen_countries

def chosen_companies():
    chosen_companies = [company['name'] for company in company_list if company['chosen']]
    return chosen_companies

def query_countries_states():
    countries = chosen_countries()
    states = chosen_states()
    companies = chosen_companies()

    conn = establish_connection()

    cursor = conn.cursor()

    query = f"SELECT symbol, comp_name, country, geo_state FROM companies Where country IN {tuple(countries)} AND geo_state IN {tuple(states)} AND comp_name IN {tuple(companies)}"

    cursor.execute(query)
    portfolio = cursor.fetchall(query)

    create_portfolio_table(portfolio)

    cursor.close()
    conn.close()

    return None

if __name__ == '__main__':
    app.run()
