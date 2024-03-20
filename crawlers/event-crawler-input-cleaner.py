import csv
from datetime import datetime as dt
from tqdm import tqdm
import pandas as pd


def processGames(game):

    if isinstance(game, str):

        league = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                              & (df['position'] == 'top')].league.values[0]
        blueteam = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                              & (df['position'] == 'top')].teamname.values[0]
        redteam = df[(df['gameid'] == game) & (df['side'] == 'Red')
                              & (df['position'] == 'top')].teamname.values[0]
        
        # WRITING TO DATASET FILE
        with open('../data/crawler/crawler-input.csv', mode='a', newline="", encoding='utf-8') as datasetSecondary2022:
            datasetWriter = csv.writer(datasetSecondary2022, delimiter=',')
            datasetWriter.writerow([game,league,blueteam,redteam,''])


df = pd.read_csv("../data/raw-2024.csv")
df22 = df.copy()
games = df22.gameid.drop_duplicates()

# Partidas já processadas pelos crawlers
processed_df = pd.read_csv("../data/crawler/crawler-input.csv")
processed_games = processed_df.game.drop_duplicates()
remaining_games = set(games) - set(processed_games)

header = 'game,league,blueteam,redteam,golId\n'
with open('../data/crawler/crawler-input.csv', mode='a', encoding='utf-8') as dataset:
    dataset.write(header)

for game in tqdm(remaining_games):    
    processGames(game)
