import csv
from datetime import datetime as dt

import pandas as pd


def processGames(game):

    if isinstance(game, str):

        datacompleteness = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                              & (df['position'] == 'top')].datacompleteness.values[0]
        league = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                              & (df['position'] == 'top')].league.values[0]
        blueteam = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                              & (df['position'] == 'top')].teamname.values[0]
        redteam = df[(df['gameid'] == game) & (df['side'] == 'Red')
                              & (df['position'] == 'top')].teamname.values[0]
        if datacompleteness != 'complete':
            return

        if processed_games.str.contains(str(game)).any() == True:
            return
        
        # WRITING TO DATASET FILE
        with open('../data/crawler/crawler-input.csv', mode='a', newline="", encoding='utf-8') as datasetSecondary2022:
            datasetWriter = csv.writer(datasetSecondary2022, delimiter=',')
            datasetWriter.writerow([game,league,blueteam,redteam,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''])


df = pd.read_csv("../data/raw.csv")
df22 = df.copy()
games = df22.gameid.drop_duplicates()

# Partidas já processadas pelos crawlers
processed_df = pd.read_csv("../data/crawler/crawler-input.csv")
processed_games = processed_df.game.drop_duplicates()

header = 'game,league,blueteam,redteam,golId,event1,event2,event3,event4,event5,event6,event7,event8,event9,event10,event11,event12,event13,event14,event15,event16,event17,event18,event19,event20,event21,event22,event23,event24,event25,event26,event27,event28,event29,event30,event31,event32,event33,event34,event35,event36,event37,event38\n'
with open('../data/crawler/crawler-input.csv', mode='a', encoding='utf-8') as dataset:
    dataset.write(header)

for game in games:    
    processGames(game)
