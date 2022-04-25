from io import BytesIO
from operator import ge
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import json
import dash.dependencies as dd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import squarify
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud


data = pd.read_csv('data.csv')
colorscales = px.colors.named_colorscales()

app = Dash()
values_year = data['Year'].unique()
values_year.sort()
values_year = list(values_year)
count_discipline = data.Sport.value_counts()
count_discipline
sns.set_style("ticks")
wordcloud = WordCloud(
    width=2000,
    height=1000,
    scale=1,
    normalize_plurals=False,
    repeat=False,
    random_state=42,
    background_color='white')
wordcloud.generate_from_frequencies(frequencies=count_discipline)
plt.figure(figsize=(17, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title('Number of athletes by sport', fontsize=30)
plt.savefig("wordcloud.png")

test_png = 'wordcloud.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

# Graph 2020
top_countries = data.Team.value_counts().sort_values(ascending=False).head(1203)
u_team = data.Team.unique()
fig_graph_2 = px.treemap(path=[u_team], values=top_countries)

app.layout = html.Div(children=[
    html.Div([
        html.H1("Welcome to Analysis of Olympics Dataset",style={"font-family":"montserrat"})
    ]),
    html.Div([
        html.H4('Enter a year you want to see the Number of Participation:',style={"font-family":"montserrat"}),
        dcc.Dropdown(
            id="dropdown",
            options=values_year,
            value="2020",
            clearable=False,
        ),
        dcc.Graph(id="graph1"),
    ]),
    html.Div([
        html.H4('The Number of the participation Country wise over the years: ->',style={"font-family":"montserrat"}),
        dcc.Graph(figure=fig_graph_2),
    ]),


    html.Div([
        html.H1("WordCloud representing the Sports",style={"font-family":"montserrat"}),
        html.Img(src='data:image/png;base64,{}'.format(test_base64),
                 style={'height': '80%', 'width': '80%', "float": "center"}),
    ])
])

# Graph 1


@app.callback(
    Output("graph1", "figure"),
    Input("dropdown", "value"))
def update_bar_chart(year):
    data_year = data.loc[data['Year'] == year]
    top_countries = data_year.Team.value_counts().sort_values(ascending=False).head(40)
    indexes = list(top_countries.keys())
    values = top_countries.values
    graph1data = pd.DataFrame({"Teams": indexes, "Participation": values})
    fig = px.bar(graph1data, x="Teams", y="Participation",
                 title='Participation', template='plotly_dark', color="Teams")
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
