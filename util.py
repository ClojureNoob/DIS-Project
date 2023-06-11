import json
import psycopg2
import plotly.graph_objs as go
import plotly.offline as opy

start_dates = ['1962-01-01']
end_dates = ['2023-01-01']

def establish_connection():
    # Load the configuration from the file
    with open('config.config', 'r') as f:
        config = json.load(f)

    # Extract the required values from the config dictionary
    db_name = config['db_name']
    db_user = config['db_user']
    pw = config['pw']
    host = config['host']
    port = config['port']

    # Establish the PostgreSQL connection
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=db_user,
        password=pw,
        options="-c client_encoding=UTF-8"
    )

    return conn

def portfolio_performance():
    conn = establish_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM portfolio')
    data = cur.fetchall()

    if len(data) == 0:
        msg = 'No portfolio data available'
    else:
        msg = ''   
    
    try:
        symbols = [row[0] for row in data]
        start_dates = [row[1] for row in data]
        end_dates = [row[2] for row in data]
        
        # Fetch portfolio performance data
        query = f"SELECT date, AVG(price) FROM prices WHERE symbol IN ({', '.join(['%s']*len(symbols))}) AND date >= %s AND date <= %s GROUP BY date ORDER BY date"
        cur.execute(query, symbols + [start_dates[0], end_dates[0]])
        performance_data = cur.fetchall()

        cur.close()
        conn.close() 

        dates = [date for date, _ in performance_data]
        average_prices = [avg_price for _, avg_price in performance_data]
        normalized_prices = [avg_price / average_prices[0] for avg_price in average_prices]

        fig = go.Figure(data=go.Scatter(x=dates, y=normalized_prices, mode='lines'))

        fig.update_layout(title='Portfolio Performance',margin=dict(l=0, r=0, t=0, b=0), width=440, height=400,paper_bgcolor="#f0f0f0")
    
        graph_html = opy.plot(fig, auto_open=False, output_type='div')

        cur.close()
        conn.close()
    except:
        fig = go.Figure(data=go.Scatter(x=[0], y=[0], mode='lines'))
        fig.update_layout(title='Portfolio Performance',margin=dict(l=0, r=0, t=0, b=0), width=440, height=400,paper_bgcolor="#f0f0f0")
        graph_html = opy.plot(fig, auto_open=False, output_type='div')


    # Render the template and pass the graph HTML to the template
    return graph_html, msg
