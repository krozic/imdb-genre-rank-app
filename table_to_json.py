import pandas as pd
import numpy as np
import json

table = pd.read_csv('./imdb_genre_rank.csv')
table = pd.read_csv('./imdb_genre_rank.csv')

genres = list(table.columns[1:])
ratings = table['rating']

genre_dict = {}

for genre in genres:
    genre_dict[genre] = {}
    for i in range(0, len(ratings)):
        rating = ratings[i]
        rank = table[genre][i]
        if not np.isnan(rank):
            genre_dict[genre][rating] = rank

# json_pretty = json.dumps(genre_dict, indent=4)

with open('imdb_genre_rank.json', 'w') as outfile:
    json.dump(genre_dict, outfile, indent=4)
