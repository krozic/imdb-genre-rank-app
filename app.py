from get_movie_rank import get_movie_rank, get_movie_info
from plotly_creator import plot_genre_dist, plot_movie_rank
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# import data:
genre_rank = pd.read_csv('./tables/genre_rank.csv')
movie_rank = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('IMDB Film Rank by Genre')
        ], width=12)
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            # html.Label('IMDB URL:'),
            html.Br(),
            dbc.Input(id='url_input', placeholder='IMDB URL', type='text'),
            # html.Br(),
            # dbc.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='output', children='Enter a link and press submit'),
        ], width=5),
        dbc.Col([
            html.Br(),
            dbc.Button('Submit', id='submit-val', n_clicks=0),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.H1(id='movie_title', children='')
        ], width=6),
        dbc.Col([
            html.H1(id='filler', children='')
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(id='poster', src='')
        ], width=6),
        dbc.Col([
            dbc.Row([
                html.H2(id='rating', children='')
            ]),
            # dbc.Row([
            #     dash_table.DataTable(movie_rank.to_dict('records'),
            #                          [{'name': i, 'id': i} for i in movie_rank.columns],
            #                          id='tbl'),
            #                          # style_header = {'backgroundColor': 'rgb(30, 30, 30)',
            #                          #                 'color': 'white'
            #                          #                 },
            #                          # style_data = {'backgroundColor': 'rgb(50, 50, 50)',
            #                          #               'color': 'white'
            #                          #               },
            #                          # ),
            # ]),
            dbc.Row([
                html.Div(id='tbl2'),
                # dbc.Table.from_dataframe(movie_rank, id='tbl1'),
            ]),
            # dash_table.DataTable(movie_rank.to_dict('records'), [{'name': i, 'id': i} for i in movie_rank.columns], id='tbl'),
        ], width=6),
        html.Br()
    ]),
    dbc.Row([
        dcc.Graph(id='ratings_distribution')
    ])
])

@app.callback(
    [Output('tbl2', 'children'),
     # Output('tbl', 'data'),
     # Output('tbl', 'columns'),
     Output('movie_title', 'children'),
     Output('poster', 'src'),
     Output('rating', 'children'),
     Output('ratings_distribution', 'figure')],
    Input('submit-val', 'n_clicks'),
    State('url_input', 'value'),
)

def update_output(n_clicks, url_input):
    if n_clicks == 0:
        movie_rank = pd.DataFrame({'Genre': [' '], 'Rank': [' ']})
        fig = plot_genre_dist(genre_rank)
        return '', '', '', '', fig
    else:
        url = url_input
        movie_info = get_movie_info(url)
        movie_rank = get_movie_rank(movie_info, genre_rank)
        fig = plot_movie_rank(movie_info, movie_rank, genre_rank)
        return dbc.Table.from_dataframe(movie_rank, hover=True), \
               movie_info['title'], \
               movie_info['poster'], \
               'Rating: {}'.format(movie_info['rating']), \
               fig

if __name__ == '__main__':
    app.run_server(debug=True)