# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Task 1: Load the dataset
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Task 2: Initialize the Dash app
app = Dash(__name__)

# Task 2: Create year list from 1980 to 2013 inclusive
year_list = [i for i in range(1980, 2014, 1)]

# Task 2: Create the app layout
app.layout = html.Div([
    html.H1('Automobile Sales Statistics Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 24}),

    html.Div([
        html.H2('Select Report Type:', style={'margin-right': '2em'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Recession Period Statistics',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),

    html.Div([
        html.H2('Select Year:', style={'margin-right': '2em'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980,
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),

    html.Div(
        id='output-container',
        className='chart-grid',
        style={'display': 'flex', 'flexDirection': 'column', 'gap': '30px', 'marginTop': '20px'}
    )
])

# Task 3: Create callback for enabling/disabling the year dropdown
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Task 4: Create callback to render charts
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter data for recession periods
        recession_data = df[df['Recession'] == 1]

        # Task 5: Plot 1: Line chart for sales over recession years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec,
                           x='Year',
                           y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation Over Recession Period (Year-wise)"))

        # Task 5: Plot 2: Bar chart for average sales by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                         x='Vehicle_Type',
                         y='Automobile_Sales',
                         title="Average Number of Vehicles Sold by Vehicle Type During Recessions"))

        # Task 5: Plot3: Pie chart for advertising expenditure share
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title="Total Expenditure Share by Vehicle Type During Recessions"))

        # Task 5: Plot4: Bar chart for unemployment rate impact
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                         x='unemployment_rate',
                         y='Automobile_Sales',
                         color='Vehicle_Type',
                         labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                         title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        # Two rows, each row contains two charts
        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex', 'gap':'20px'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex', 'gap':'20px'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year is not None:
        # Filter data for selected single year
        yearly_data = df[df['Year'] == input_year]

        # Task 6: Plot1: Full period yearly automobile sales
        Y_chart1 = dcc.Graph(
            figure=px.line(df.groupby('Year')['Automobile_Sales'].mean().reset_index(),
                           x='Year',
                           y='Automobile_Sales',
                           title='Yearly Automobile Sales for the Whole Period'))

        # Task 6: Plot2: Monthly sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           title='Total Monthly Automobile Sales'))

        # Task 6: Plot3: Average sales by vehicle type for selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata,
                         x='Vehicle_Type',
                         y='Automobile_Sales',
                         title=f'Average Vehicles Sold by Vehicle Type in the year {input_year}'))

        # Task 6: Plot4: Pie chart of ad expenditure
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                          values='Advertising_Expenditure',
                          names='Vehicle_Type',
                          title='Total Advertisement Expenditure for Each Vehicle'))

        # Two rows, each row contains two charts
        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex', 'gap':'20px'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex', 'gap':'20px'})
        ]
    else:
        # Return empty when no valid selection
        return []

if __name__ == '__main__':
    app.run(debug=True)
