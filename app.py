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

test_png = 'yy.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

# Graph 2020
top_countries = data.Team.value_counts().sort_values(ascending=False).head(1203)
u_team = data.Team.unique()
fig_graph_2 = px.treemap(path=[u_team], values=top_countries,
                         color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")

# Graph Age_Medal
data_age = list(data.Age)
data_medal = list(data.Medal)
for i in range(len(data_medal)):
    if(data_medal[i] > 0):
        data_medal[i] = 1

data_pie = pd.DataFrame({"Age": data_age, "Medal": data_medal})
result = data_pie.sort_values('Age')
result.drop(result[result['Age'] > 70].index, inplace=True)
fig_age_medal = px.pie(result, values='Medal', names='Age',
                       title="Age-Medal Distribution", color_discrete_sequence=px.colors.sequential.RdBu,
                       hover_data=['Age'], template="plotly_dark",)
fig_age_medal.update_traces(textposition='inside', textinfo='percent+label')
fig_age_medal.update_layout(margin=dict(t=30, b=30, l=30, r=30))


df = pd.read_csv('athlete_events.csv',error_bad_lines=False, engine="python")
newdf=df.groupby('Team').Medal.value_counts().unstack().fillna(0)
topc=newdf.loc[newdf['Silver'] >= 300]
bottomc=newdf.loc[newdf['Silver'] <= 150 ]
bottomc=newdf.sample(n=10)
frames = [topc, bottomc]
result = pd.concat(frames)
result=result.sample(frac = 1)
fig_heatmap=px.imshow(result,text_auto=True,width=800,height=400,template="plotly_dark")
fig_heatmap.layout.height = 800
fig_heatmap.layout.width = 800



# Graph Gender Wise and Medal Distribution
values_gender = ["Male", "Female"]

# Graph Season Wise and M/F Distribution
values_season = ["Summer", "Winter"]

app.layout = html.Div(style={'backgroundColor': 'black'}, children=[
    html.Div([
        html.H1("Welcome to Analysis of Olympics Dataset", style={
                "font-family": "montserrat", "color": "white", "text-align": "center"})
    ]),
    html.Div([
        html.H4('Enter a year you want to see the Number of Participation:', style={
                "font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Dropdown(
            id="dropdown",
            options=values_year,
            clearable=False,
            style={"background-color": "black",
                   "text": "white", "text-align": "center"}
        ),
        dcc.Graph(id="graph1",
                  figure={
                      'layout': {
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
        html.H4('The Age - Medal Distribution',
                style={"font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Graph(figure=fig_age_medal),
    ]),
    html.Div([
        html.H4('The Number of the participation Country wise over the years: ->',
                style={"font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Graph(figure=fig_graph_2),
    ]),
    html.Div([
        html.H4('The Number of Medals versus Certain Countries: ->',
                style={"font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Graph(figure=fig_heatmap,
        style={"align":'center','width':'100%'}),
    ]),

    html.Div([
        html.H1('Gender Wise Distribution of Medal', style={
                "font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Dropdown(
            id="gender_dropdown",
            options=values_gender,
            clearable=False,
            style={"background-color": "black",
                   "text": "white", "text-align": "center"}
        ),
        dcc.Graph(id="graph_gender",
                  figure={
                      'layout': {
                          'plot_bgcolor': colors['background'],
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                      }
                  }
                  ),
        dcc.Graph(id="graph_participation",
                  figure={
                      'layout': {
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
        html.H4('Enter The season you want to see the Number of Participation:', style={
                "font-family": "montserrat", "color": "white", "text-align": "center"}),
        dcc.Dropdown(
            id="values_season",
            options=values_season,
            clearable=False,
            style={"background-color": "black",
                   "text": "white", "text-align": "center"}
        ),
        dcc.Graph(id="graph_season",
                  figure={
                      'layout': {
                          'plot_bgcolor': colors['background'],
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                      }
                  }
                  ),
    ]),
    html.Div([
        html.H1("WordCloud representing the Sports", style={
                "font-family": "montserrat", "color": "white", "text-align": "center"}),
        html.Img(src='data:image/png;base64,{}'.format(test_base64),
                 style={'height': '50%', 'width': '50%', "display": "block", "margin-left": "auto", "margin-right": "auto",
                 "width": "50%"}),
    ]),
    html.Div([
        html.H4("Created by Pratham Agrawal", style={
            "font-family": "montserrat", "color": "white", "text-align": "center"
        })
    ])
])

# Graph 1
@ app.callback(
    Output("graph1", "figure"),
    Input("dropdown", "value"))
def update_bar_chart(year):
    data_year = data.loc[data['Year'] == year]
    top_countries = data_year.Team.value_counts().sort_values(ascending=False).head(40)
    indexes = list(top_countries.keys())
    values = top_countries.values
    graph1data = pd.DataFrame({"Teams": indexes, "Participation": values})
    fig = px.bar(graph1data, x="Teams", y="Participation",
                 title='Participation', template='plotly_dark', color="Teams", color_discrete_sequence=px.colors.sequential.RdBu)
    return fig


# Graph Male - Female Medal Distribution
@ app.callback(
    Output("graph_gender", "figure"),
    Input("gender_dropdown", "value"))
def update_gender(gender):
    data['Sex'] = data['Sex'].replace("M", "Male")
    data['Sex'] = data['Sex'].replace("F", "Female")
    data_male = data.loc[data['Sex'] == gender]

    medal_male = list(data_male['Medal'])
    for i in range(len(medal_male)):
        medal_male[i] = int(medal_male[i])

    medal_male_no = medal_male.count(0)
    medal_male_bronze = medal_male.count(1)
    medal_male_silver = medal_male.count(2)
    medal_male_gold = medal_male.count(3)
    medal_count = [medal_male_no, medal_male_bronze,
                   medal_male_silver, medal_male_gold]
    fig = px.pie(values=medal_count, names=["No Medal", "Bronze", "Silver", "Gold"],
                 color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark")
    return fig


# Graph MenOverTime
@app.callback(
    Output("graph_participation", "figure"),
    Input("gender_dropdown", "value"))
def update_box(gender):
    data['Sex'] = data['Sex'].replace("M", "Male")
    data['Sex'] = data['Sex'].replace("F", "Female")
    MenOverTime = data[(data.Sex == gender) & (data.Season == 'Summer')]

    fig = px.box(MenOverTime, x='Year', y='Age', hover_name='Year',
                 color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark",
                 title="Variation of Age for "+str(gender)+" Athletes over time")
    fig.update_traces(quartilemethod="inclusive")
    return fig


# Graph SummerWinter Season
@app.callback(
    Output("graph_season", "figure"),
    Input("values_season", "value"))
def update_Season(season):
    data = pd.read_csv("data.csv")
    data.rename({'Unnamed: 0': 'ID'}, axis=1, inplace=True)
    summer_olympic = data.query("Season =='Summer'")
    winter_olympic = data.query("Season =='Winter'")
    games = {"Summer": summer_olympic, "Winter": winter_olympic}
    sex_year_df = games[season].groupby(["Year", "Sex"]).ID.count().rename("Count").reset_index()
    sex_year_df = sex_year_df.pivot(
        index="Year", columns="Sex", values="Count").reset_index()
    sex_year_df["Ratio"] = sex_year_df["M"] / sex_year_df["F"]
    fig = px.line(sex_year_df, x="Year", y="Ratio", title=str(season)+" Olympic Games M/F Ratio Over Years",
                  color_discrete_sequence=px.colors.sequential.RdBu, template="plotly_dark",)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
