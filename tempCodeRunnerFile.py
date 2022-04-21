from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import json


data = pd.read_csv('data.csv')

app = Dash()
geo_dropdown = dcc.Dropdown(options=data['Year'].unique(),
                            value='New York')

app.layout = html.Div(children=[html.H1(
    children='Dashboard'), geo_dropdown, dcc.Graph(id='price-graph')])


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    filtered_data = data[data['Year'] == selected_geography]
    line_fig = px.bar(filtered_data,
                       x='Age', y='Medal',
                       color='Team',
                       title=f'No. of Medals won by a Country in {selected_geography}')
    return line_fig



if __name__ == '__main__':
    app.run_server(debug=True)