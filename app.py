import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

def generate_table(dataframe, max_rows=600):
    # dataframe = pd.read_sql_query("select * from janjuncriticas;", conn)

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# Launch the application:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

# config
app.secret_key = 'my secret key'

try:
  conn = mysql.connector.connect(
    user='dabago', 
    password='integration',
    host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
    port=3306,
    database='root')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
    
    
#dfaltas = pd.read_sql_query("select * from janjunaltas;", conn)
dfa = pd.read_sql_query("select * from ultrasincomas where Priority = 'High'", conn)
dfaltas = dfa[['Incident ID', 'Month','Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]

dfc = pd.read_sql_query("select * from ultrasincomas where Priority = 'Critical'", conn)
dfcriticas = dfc[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]

# Load table critical dash
#df = pd.read_sql_query("select * from janjuncriticas;", conn)

options_critical_table =[] 
for service in dfcriticas['Month'].unique():
    options_critical_table.append({'label':service,'value':service})

table_criticas_layout = html.Div(children=[
    html.H4(children='Critical incidences per month - Details'),
    dcc.Dropdown(id='dropdown', options=
    options_critical_table, 
    multi=True, placeholder='Filter by Month'),
    html.Div(id='table-container')
])

@app.callback(
    dash.dependencies.Output('table-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table(dropdown_value):
    if dropdown_value is None:
        conn = mysql.connector.connect(
        user='dabago', 
        password='integration',
        host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
        port=3306,
        database='root')
            
        dfc = pd.read_sql_query("select * from ultrasincomas where Priority = 'Critical'", conn)
        dfcriticas = dfc[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]        
        return generate_table(dfcriticas)

    conn = mysql.connector.connect(
    user='dabago', 
    password='integration',
    host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
    port=3306,
    database='root')
    df = pd.read_sql_query("select * from ultrasincomas;", conn)
    dfc = df[df['Priority'] == 'Critical']
    dfcriticas = dfc[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
    dff = dfcriticas[dfcriticas['Month'].str.contains('|'.join(dropdown_value))]
    return generate_table(dff)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Load table altas dash

def generate_table_altas(dataframe, max_rows=600):
#    dfaltas = dfnewaltas.copy()

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

table_altas_layout = html.Div(children=[
    html.H4(children='High incidences per month - Details'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in dfaltas.Month.unique()
    ], multi=True, placeholder='Filter by Month'),
    html.Div(id='table-container-altas')
])

@app.callback(
    dash.dependencies.Output('table-container-altas', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table_altas(dropdown_value):
    if dropdown_value is None:
        conn = mysql.connector.connect(
        user='dabago', 
        password='integration',
        host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
        port=3306,
        database='root')
        
        dfa = pd.read_sql_query("select * from ultrasincomas where Priority = 'High'", conn)
        dfaltas = dfa[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
        return generate_table_altas(dfaltas)
    conn = mysql.connector.connect(
    user='dabago', 
    password='integration',
    host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
    port=3306,
    database='root')
    dfa = pd.read_sql_query("select * from ultrasincomas where Priority = 'High'", conn)
    dfaltas = dfa[['Incident ID', 'Month','Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
    dff_altas = dfaltas[dfaltas.Month.str.contains('|'.join(dropdown_value))]
    return generate_table_altas(dff_altas)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

############################### medium

def generate_table_medium(dataframe, max_rows=600):
#    dfaltas = dfnewaltas.copy()

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

table_medium_layout = html.Div(children=[
    html.H4(children='Medium incidences per month - Details'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in dfaltas.Month.unique()
    ], multi=True, placeholder='Filter by Month'),
    html.Div(id='table-container-medium')
])

@app.callback(
    dash.dependencies.Output('table-container-medium', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table_medium(dropdown_value):
    if dropdown_value is None:
        conn = mysql.connector.connect(
        user='dabago', 
        password='integration',
        host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
        port=3306,
        database='root')
        
        dfm = pd.read_sql_query("select * from ultrasincomas where Priority = 'Medium'", conn)
        dfmedium = dfm[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
        return generate_table_medium(dfmedium)
    conn = mysql.connector.connect(
    user='dabago', 
    password='integration',
    host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
    port=3306,
    database='root')
    dfm = pd.read_sql_query("select * from ultrasincomas where Priority = 'Medium'", conn)
    dfmedium = dfm[['Incident ID', 'Month','Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
    dff_medium = dfmedium[dfmedium.Month.str.contains('|'.join(dropdown_value))]
    return generate_table_medium(dff_medium)

############################### low

def generate_table_low(dataframe, max_rows=600):
#    dfaltas = dfnewaltas.copy()

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

table_low_layout = html.Div(children=[
    html.H4(children='low incidences per month - Details'),
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in dfaltas.Month.unique()
    ], multi=True, placeholder='Filter by Month'),
    html.Div(id='table-container-low')
])

@app.callback(
    dash.dependencies.Output('table-container-low', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def display_table_low(dropdown_value):
    if dropdown_value is None:
        conn = mysql.connector.connect(
        user='dabago', 
        password='integration',
        host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
        port=3306,
        database='root')
        
        dfl = pd.read_sql_query("select * from ultrasincomas where Priority = 'Low'", conn)
        dflow = dfl[['Incident ID','Month', 'Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
        return generate_table_low(dflow)
    conn = mysql.connector.connect(
    user='dabago', 
    password='integration',
    host='db.cqpvfmmecqgi.us-east-1.rds.amazonaws.com',
    port=3306,
    database='root')
    dfl = pd.read_sql_query("select * from ultrasincomas where Priority = 'Low'", conn)
    dflow = dfl[['Incident ID', 'Month','Date raised', 'Date closed', 'Service',  'Priority','Status', 'Tower Group' , 'MTTR general']]
    dff_low = dflow[dflow.Month.str.contains('|'.join(dropdown_value))]
    return generate_table_low(dff_low)
## Create a DataFrame criticas:
#df2 = pd.read_sql_query("select * from janjuncriticas;", conn)
#
#critical_inc = df2.copy()
#
#jan_inc= critical_inc[critical_inc["Month"] == "January"]
#jan_inc['date'] = pd.DatetimeIndex(jan_inc['Date raised']).date
#jan_count = jan_inc.groupby(['Application'])[['Incident ID']].nunique()
#jan_count["Application"]= jan_count.index
#
#feb_inc= critical_inc[critical_inc["Month"] == "February"]
#feb_inc['date'] = pd.DatetimeIndex(feb_inc['Date raised']).date
#
#feb_count = feb_inc.groupby(['Application'])[['Incident ID']].nunique()
#feb_count["Application"]= feb_count.index
#
#mar_inc= critical_inc[critical_inc["Month"] == "March"]
#mar_inc['date'] = pd.DatetimeIndex(mar_inc['Date raised']).date
#
#mar_count = mar_inc.groupby(['Application'])[['Incident ID']].nunique()
#mar_count["Application"]= mar_count.index
#
#apr_inc= critical_inc[critical_inc["Month"] == "April"]
#apr_inc['date'] = pd.DatetimeIndex(apr_inc['Date raised']).date
#
#apr_count = apr_inc.groupby(['Application'])[['Incident ID']].nunique()
#apr_count["Application"]= apr_count.index
#
#may_inc= critical_inc[critical_inc["Month"] == "May"]
#may_inc['date'] = pd.DatetimeIndex(may_inc['Date raised']).date
#
#may_count = may_inc.groupby(['Application'])[['Incident ID']].nunique()
#may_count["Application"]= may_count.index
#
#jun_inc= critical_inc[critical_inc["Month"] == "June"]
#jun_inc['date'] = pd.DatetimeIndex(jun_inc['Date raised']).date
#
#jun_count = jun_inc.groupby(['Application'])[['Incident ID']].nunique()
#jun_count["Application"]= jun_count.index
#
#trace1 = go.Bar(
#    x=jan_count['Application'],  
#    y=jan_count['Incident ID'],
#    name = 'January',
#    marker=dict(color='#FFD700') 
#)
#trace2 = go.Bar(
#    x=feb_count['Application'],
#    y=feb_count['Incident ID'],
#    name='February',
#    marker=dict(color='#9EA0A1') 
#)
#trace3 = go.Bar(
#    x=mar_count['Application'],
#    y=mar_count['Incident ID'],
#    name='March',
#    marker=dict(color='#CD7F32') 
#)
#trace4 = go.Bar(
#    x=apr_count['Application'],  
#    y=apr_count['Incident ID'],
#    name = 'April',
#    marker=dict(color='#DF0101') 
#)
#trace5 = go.Bar(
#    x=may_count['Application'],
#    y=may_count['Incident ID'],
#    name='May',
#    marker=dict(color='#3B0B39') 
#)
#trace6 = go.Bar(
#    x=jun_count['Application'],
#    y=jun_count['Incident ID'],
#    name='June',
#    marker=dict(color='#4B8A08') 
#)
#data = [trace1, trace2, trace3, trace4, trace5, trace6]
#
## Create a Dash layout that contains a Graph component:
#graph_criticas_layout = html.Div([
#    dcc.Graph(
#        id='critical-incs-by-app-jan-to-jun',
#        figure={
#            'data': data,
#            'layout': go.Layout(
#                title = 'Critical Incidences raised by Application',
#                yaxis = {'title': 'Number of incidences'},
#                barmode='stack',
#                showlegend=True,
#                legend=go.layout.Legend(
#                    x=0,
#                    y=1.0
#                ),
#                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
#            )
#        }
#    )
#])

# Create a DataFrame criticas:
#dfaltas = pd.read_sql_query("select * from janjunaltas;", conn)
#
#inc_altas = dfaltas.copy()
#
#jan_inc_altas= inc_altas[inc_altas["Month"] == "January"]
#jan_inc_altas['date'] = pd.DatetimeIndex(jan_inc_altas['Date raised']).date
#jan_count_altas = jan_inc_altas.groupby(['Application'])[['Incident ID']].nunique()
#jan_count_altas["Application"]= jan_count_altas.index
#
#feb_inc_altas= inc_altas[inc_altas["Month"] == "February"]
#feb_inc_altas['date'] = pd.DatetimeIndex(feb_inc_altas['Date raised']).date
#
#feb_count_altas = feb_inc_altas.groupby(['Application'])[['Incident ID']].nunique()
#feb_count_altas["Application"]= feb_count_altas.index
#
#mar_inc_altas= inc_altas[inc_altas["Month"] == "March"]
#mar_inc_altas['date'] = pd.DatetimeIndex(mar_inc_altas['Date raised']).date
#
#mar_count_altas = mar_inc_altas.groupby(['Application'])[['Incident ID']].nunique()
#mar_count_altas["Application"]= mar_count_altas.index
#
#apr_inc_altas= inc_altas[inc_altas["Month"] == "April"]
#apr_inc_altas['date'] = pd.DatetimeIndex(apr_inc_altas['Date raised']).date
#
#apr_count_altas = apr_inc.groupby(['Application'])[['Incident ID']].nunique()
#apr_count_altas["Application"]= apr_count_altas.index
#
#may_inc_altas= inc_altas[inc_altas["Month"] == "May"]
#may_inc_altas['date'] = pd.DatetimeIndex(may_inc_altas['Date raised']).date
#
#may_count_altas = may_inc_altas.groupby(['Application'])[['Incident ID']].nunique()
#may_count_altas["Application"]= may_count_altas.index
#
#jun_inc_altas= inc_altas[inc_altas["Month"] == "June"]
#jun_inc_altas['date'] = pd.DatetimeIndex(jun_inc_altas['Date raised']).date
#
#jun_count_altas = jun_inc_altas.groupby(['Application'])[['Incident ID']].nunique()
#jun_count_altas["Application"]= jun_count_altas.index
#
#trace1altas = go.Bar(
#    x=jan_count_altas['Application'],  
#    y=jan_count_altas['Incident ID'],
#    name = 'January',
#    marker=dict(color='#FFD700') 
#)
#trace2altas = go.Bar(
#    x=feb_count_altas['Application'],
#    y=feb_count_altas['Incident ID'],
#    name='February',
#    marker=dict(color='#9EA0A1') 
#)
#trace3altas = go.Bar(
#    x=mar_count_altas['Application'],
#    y=mar_count_altas['Incident ID'],
#    name='March',
#    marker=dict(color='#CD7F32') 
#)
#trace4altas = go.Bar(
#    x=apr_count_altas['Application'],  
#    y=apr_count_altas['Incident ID'],
#    name = 'April',
#    marker=dict(color='#DF0101') 
#)
#trace5altas = go.Bar(
#    x=may_count_altas['Application'],
#    y=may_count_altas['Incident ID'],
#    name='May',
#    marker=dict(color='#3B0B39') 
#)
#trace6altas = go.Bar(
#    x=jun_count_altas['Application'],
#    y=jun_count_altas['Incident ID'],
#    name='June',
#    marker=dict(color='#4B8A08') 
#)
#data_altas = [trace1altas, trace2altas, trace3altas, trace4altas, trace5altas, trace6altas]
#
## Create a Dash layout that contains a Graph component:
#graph_altas_layout = html.Div([
#    dcc.Graph(
#        id='high-incs-by-app-jan-to-jun',
#        figure={
#            'data': data_altas,
#            'layout': go.Layout(
#                title = 'High Incidences raised by Application',
#                yaxis = {'title': 'Number of incidences'},
#                barmode='stack',
#                showlegend=True,
#                legend=go.layout.Legend(
#                    x=0,
#                    y=1.0
#                ),
#                margin=go.layout.Margin(l=100, r=0, t=100, b=100)
#            )
#        }
#    )
#])
#
# Load table dash
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == '/graph-criticas':
    #     return graph_criticas_layout
    if pathname == '/table-criticas':
        return table_criticas_layout
    elif pathname == '/table-altas':
        return table_altas_layout
    elif pathname == '/table-medium':
        return table_medium_layout
    elif pathname == '/table-low':
        return table_low_layout

    # elif pathname == '/graph-altas':
    #     return graph_altas_layout
    # else:
    return "URL not found"
    # You could also return a 404 "URL not found" page here

# Add the server clause:
if __name__ == '__main__':
    df = pd.read_sql_query("select * from ultrasincomas;", conn)
    app.run_server(debug=True)
    