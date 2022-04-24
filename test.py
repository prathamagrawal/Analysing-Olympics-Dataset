
app.layout = html.Div([
    html.H4('Restaurant tips by day of week'),
    dcc.Dropdown(
        id="dropdown",
        options=geo_dropdown,
        value="Fri",
        clearable=False,
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart(day):
    df = px.data.tips() # replace with your own data source
    mask = data["Team"] == day
    fig = px.bar(data[mask], x="sex", y="total_bill", 
                 color="smoker", barmode="group")
    return fig


app.run_server(debug=True)



year=2020
data_year = data.loc[data['Year'] == year]
top_countries=data_year.Team.value_counts().sort_values(ascending=False).head(20)
top_countries


sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

plt.figure(figsize=(12,6))
plt.xticks(rotation=75)
plt.title('Overall Participation Countrywise in '+str(year))
fig1=sns.barplot(x=top_countries.index, y=top_countries);

app.layout = html.Div(children=[
    html.H1(children='Sales Funnel Report'),
    html.Div(children='''National Sales Funnel Report.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': fig1,
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
])