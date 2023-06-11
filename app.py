from flask import Flask, render_template, send_file, request, jsonify
from us_states import states
from countries import country_list
from companies import company_list
import psycopg2
from util import establish_connection, portfolio_performance
import datetime
import plotly.graph_objs as go
import plotly.offline as opy

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
    names = [name[0].replace(',','') for name in cursor.fetchall()]

    query = "SELECT symbol FROM companies;"
    cursor.execute(query)
    symbols = [symbol[0] for symbol in cursor.fetchall()]

    #----------Price data ------------
    query = "SELECT date, close FROM aapl;"

    cursor.close()
    conn.close()

    graph_html,msg = portfolio_performance()
    
    return render_template('content.html',coordinates=coordinates, names=names,symbols=symbols, graph_html=graph_html, msg=msg, country_list=country_list, states=states, company_list=company_list) 

@app.route('/update', methods=['GET', 'POST'])
def update_chosen():
    """
    Keeps track os states, countries and companies and update their status whether they have been chosen by the user.
    """

    if request.method == 'POST':
        chosen_state = request.form.get('state')
        for state in states:
            if state['name'] == chosen_state:
                state['chosen'] = True
            else:
                state['chosen'] = False

    if request.method == 'POST':
        chosen_country = request.form.get('country')
        for country in country_list:
            if country['name'] == chosen_country:
                country['chosen'] = True
            else:
                country['chosen'] = False

    if request.method == 'POST':
        chosen_companies = request.form.get('company')
        for company in company_list:
            if company['company_name'] == chosen_companies:
                company['Chosen'] = True
            else:
                company['Chosen'] = False

    render_map()

    return '0'





def create_portfolio_table(portfolio, start_date, end_date):
    """
    The strategy is to first find all tags to include in the query, through all three choices
    Then exact the date 
    Then commit the query, filtering by date and tags
    """
    symbols = [row[0] for row in portfolio] # List of all symbols to extract

    conn = establish_connection()
    cursor = conn.cursor()

    # We delete the existing table if it exists
    cursor.execute("DROP TABLE IF EXISTS portfolio;")

    # We create a table 
    cursor.execute(f"CREATE TABLE portfolio (symbol VARCHAR(10), start_date DATE, end_date DATE);")
    
    #Insert all symbols in symbols into the table with start_date and end_date
    filtered_rows = [(symbol, start_date, end_date) for symbol in symbols]
    cursor.executemany("INSERT INTO portfolio (symbol, start_date, end_date) VALUES (%s, %s, %s)", filtered_rows)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return None

def chosen_states():
    chosen_states = [state['name'] for state in states if state['chosen']]
    return chosen_states

def chosen_countries():
    chosen_countries = [country['name'] for country in country_list if country['chosen']]
    return chosen_countries

def chosen_companies():
    chosen_companies = [company['company_name'] for company in company_list if company['Chosen']]
    return chosen_companies


def create_table(name, content):
    conn = establish_connection()
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {name};")

    query = f"CREATE TABLE {name} (Names TEXT);"

    cursor.execute(query)

    for value in content:
        cursor.execute(f"INSERT INTO {name} (Names) VALUES ('{value}')")

    conn.commit()
    cursor.close()
    conn.close()

def query_countries_states(countries, states, companies, start_date, end_date):
    countries = chosen_countries() # list of all countries chosen
    states = chosen_states() # list of all states chosen
    companies = chosen_companies() # list of all companies chosen

    create_table('Temp1', countries)
    create_table('Temp2', states)
    create_table('Temp3', companies)

    conn = establish_connection()

    cursor = conn.cursor()

    query = "SELECT symbol, comp_name, country, geo_state FROM companies WHERE country IN " + "(SELECT Names FROM Temp1)" + " AND geo_state IN " + "(SELECT Names FROM Temp2)" + " AND comp_name IN " + "(SELECT Names FROM Temp3)" + ";"

    cursor.execute(query)
    portfolio = cursor.fetchall() # Returns a list of tuples, where each tuple corresponds to a row in the database

    create_portfolio_table(portfolio, start_date, end_date)


    conn.commit()
    cursor.close()
    conn.close()

    return None

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()

    # Extract the necessary parameters from the data dictionary
    countries = data.get('country')
    states = data.get('state')
    companies = data.get('company')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    # Perform the query_countries_states function with the extracted parameters
    query_countries_states(countries, states, companies, start_date, end_date)

    # Return a JSON response indicating success
    response = {'message': 'Query executed successfully'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)