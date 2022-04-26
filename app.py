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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


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
    background_color='black')
wordcloud.generate_from_frequencies(frequencies=count_discipline)
plt.figure(figsize=(17, 10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordcloud.png")

test_png = 'wordcloud.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

# Graph 2020
top_countries = data.Team.value_counts().sort_values(ascending=False).head(1203)
u_team = data.Team.unique()
fig_graph_2 = px.treemap(path=[u_team], values=top_countries,color_discrete_sequence=px.colors.sequential.RdBu,template="plotly_dark")

#Graph Age_Medal
data_age=list(data.Age)
data_medal=list(data.Medal)
for i in range(len(data_medal)):
    if(data_medal[i]>0):
        data_medal[i]=1

data_pie=pd.DataFrame({"Age":data_age, "Medal":data_medal})
result=data_pie.sort_values('Age')
result.drop(result[result['Age'] > 70].index, inplace = True)
fig_age_medal = px.pie(result, values='Medal', names='Age',
    title="Age-Medal Distribution",color_discrete_sequence=px.colors.sequential.RdBu,
    hover_data=['Age'],template = "plotly_dark",)
fig_age_medal.update_traces(textposition='inside', textinfo='percent+label')
fig_age_medal.update_layout(margin=dict(t=30, b=30, l=30, r=30))


app.layout = html.Div(style={'backgroundColor': colors['background'],'margin-left':"0px"},children=[
    html.Div([
        html.H1("Welcome to Analysis of Olympics Dataset",style={"font-family":"montserrat","color":"white"})
    ]),
    html.Div([
        html.H4('Enter a year you want to see the Number of Participation:',style={"font-family":"montserrat","color":"white"}),
        dcc.Dropdown(
            id="dropdown",
            options=values_year,
            clearable=False,
            style = {"background-color":"black","text":"white"}
        ),
        dcc.Graph(id="graph1",
            figure={
                'layout':{
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
    ]),
    html.Div([
        html.H4('The Age - Medal Distribution',style={"font-family":"montserrat","color":"white"}),
        dcc.Graph(figure=fig_age_medal),
    ]),
    html.Div([
        html.H4('The Number of the participation Country wise over the years: ->',style={"font-family":"montserrat","color":"white"}),
        dcc.Graph(figure=fig_graph_2),
    ]),
    html.Div([
        html.H1("WordCloud representing the Sports",style={"font-family":"montserrat","color":"white"}),
        html.Img(src='data:image/png;base64,{}'.format(test_base64),
                 style={'height': '100%', 'width': '100%', "float": "center"}),
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
                 title='Participation', template='plotly_dark', color="Teams",color_discrete_sequence=px.colors.sequential.RdBu)
    return fig



# Graph Male - Female Medal Distribution 



if __name__ == '__main__':
    app.run_server(debug=True)
