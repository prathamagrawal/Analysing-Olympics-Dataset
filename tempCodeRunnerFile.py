from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

avocado = pd.read_csv('data.csv')