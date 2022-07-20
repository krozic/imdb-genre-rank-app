import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any

with open('./tables/genre_rank.csv', 'r') as filehandle:
    genre_rank = pd.read_csv(filehandle)

def plot_genre_dist(genre_rank: pd.DataFrame):
    fig = go.Figure()
    for genre in genre_rank.columns[1:]:
        genre_plot = genre_rank[['averageRating', genre]].dropna()
        fig.add_trace(go.Scatter(x=genre_plot['averageRating'],
                                 y=genre_plot[genre],
                                 name=genre,
                                 mode='lines'))
    return fig

def plot_movie_rank(movie_info: Dict[str, Any], movie_rank: pd.DataFrame, genre_rank: pd.DataFrame):
    fig = go.Figure()
    for genre in genre_rank.columns[1:]:
        genre_plot = genre_rank[['averageRating', genre]].dropna()
        fig.add_trace(go.Scatter(x=genre_plot['averageRating'],
                                 y=genre_plot[genre],
                                 name=genre,
                                 mode='lines'))

    genres = list(movie_rank['Genre'])
    fig.for_each_trace(lambda trace: trace.update(visible='legendonly')
    if trace.name not in genres else ())
    x = []
    for genre in genres:
        x.append(movie_info['rating'])

    fig.add_trace(go.Scatter(x=x,
                             y=movie_rank['Rank'],
                             name='query',
                             mode='markers',
                             marker=dict(size=[10, 10, 10], color=[3, 3, 3])))
    return fig