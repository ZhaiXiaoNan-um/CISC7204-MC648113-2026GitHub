#1/Import dataset
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

airline_data = pd.read_csv('airline_data.csv',
                           encoding = "ISO-8859-1",
                           dtype={'Div1Airport': str, 'Div1TailNum': str,
                                  'Div2Airport': str, 'Div2TailNum': str})

#2/ Give the title to the dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Total number of flights to the destination state split by reporting airline',
            style={'fontSize':40}),
    html.Div([
        html.Div('Input Year: ', style={'fontSize':40}),
        dcc.Input(id='input-year', value=2010, type='number',
                  style={'height':'50px','fontSize':35})
    ], style={'fontSize':35}),
    dcc.Graph(id='bar-plot')
])

# 3/ Add Callback decorator
@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='input-year', component_property='value')
)

#4/ Define Callback graph function
def get_graph(entered_year):
    df = airline_data[airline_data['Year'] == entered_year]
    bar_data = df.groupby(['DestState','Reporting_Airline'])['Flights'].sum().reset_index()
    fig = px.bar(bar_data, x='DestState', y='Flights', color='Reporting_Airline',
                 title='Flights to Destination State')
    return fig

#5/running the app
if __name__ == '__main__':
    app.run()
