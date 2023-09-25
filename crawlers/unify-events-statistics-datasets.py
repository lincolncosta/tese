import pandas as pd
import numpy as np

statistics_df = pd.read_csv("../data/crawler/players_statistics-2023.csv")
events_output_df = pd.read_csv("../data/crawler/crawler-output-2023.csv")
events_input_df = pd.read_csv("../data/crawler/crawler-input-2023.csv")
gameIds = []

for index, row in events_output_df.iterrows():
    golId = row['golId']

    if np.isfinite(golId):
        filtered_df = events_input_df.loc[events_input_df['golId'] == golId]
        game = filtered_df['game'].values[0]
        gameIds.append(game)

events_output_df.insert(1, 'game', gameIds)

unified_df = pd.merge(events_output_df, statistics_df, on="game")
unified_df.to_csv("../data/crawler/unified-events-statistics-2023.csv", index=False)