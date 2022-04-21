from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import json


data = pd.read_csv('data.csv')

app = Dash()
geo_dropdown = dcc.Dropdown(options=data['Year'].unique(),
                            value='New York')


@app.callback(
    Output(component_id='graph-02', component_property='figure'),
    Input(component_id=geo_dropdown, component_property='value')
)
def update_graph(selected_geography):
    filtered_data = data[data['Year'] == selected_geography]
    line_fig = px.bar(filtered_data,
                       x='Age', y='Medal',
                       color='Team',
                       title=f'No. of Medals won by a Country in {selected_geography}')
    return line_fig



fig = px.choropleth(locationmode="USA-states", color=[1], scope="usa")
 

#app.layout = html.Div(childern=[dcc.Graph(id="life-exp-vs-gdp", figure=fig),[html.H1(children='Dashboard'), geo_dropdown, dcc.Graph(id='price-graph')])])

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Dashboard- Graph 01'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Graph 02'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        geo_dropdown,
        dcc.Graph(
            id='graph-02',
            figure=fig
        ),  
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)