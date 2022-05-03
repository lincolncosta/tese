import pandas as pd
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
from datetime import datetime as dt
import csv


def processGames(game, side):

    if isinstance(game, str):

        datacompleteness = df[(df['gameid'] == game) & (df['side'] == side)
                              & (df['position'] == 'top')].datacompleteness.values[0]
        if datacompleteness != 'complete':
            return

        # BLUE TEAM
        top = df[(df['gameid'] == game) & (df['side'] == side)
                 & (df['position'] == 'top')].champion.values[0]
        topPlayer = df[(df['gameid'] == game) & (df['side'] == side) & (
            df['position'] == 'top')].playername.values[0]
        if (topPlayer != 'unknown player'):
            top = int(
                df_champions.loc[df_champions['id'] == top]['key'])
        else:
            return

        jungle = df[(df['gameid'] == game) & (df['side'] == side) & (
            df['position'] == 'jng')].champion.values[0]
        junglePlayer = df[(df['gameid'] == game) & (
            df['side'] == side) & (df['position'] == 'jng')].playername.values[0]
        if (junglePlayer != 'unknown player'):
            jungle = int(
                df_champions.loc[df_champions['id'] == jungle]['key'])
        else:
            return

        mid = df[(df['gameid'] == game) & (df['side'] == side)
                 & (df['position'] == 'mid')].champion.values[0]
        midPlayer = df[(df['gameid'] == game) & (df['side'] == side) & (
            df['position'] == 'mid')].playername.values[0]
        if (midPlayer != 'unknown player'):
            mid = int(
                df_champions.loc[df_champions['id'] == mid]['key'])
        else:
            return

        carry = df[(df['gameid'] == game) & (df['side'] == side) & (
            df['position'] == 'bot')].champion.values[0]
        carryPlayer = df[(df['gameid'] == game) & (
            df['side'] == side) & (df['position'] == 'bot')].playername.values[0]
        if (carryPlayer != 'unknown player'):
            carry = int(
                df_champions.loc[df_champions['id'] == carry]['key'])
        else:
            return

        supp = df[(df['gameid'] == game) & (df['side'] == side) & (
            df['position'] == 'sup')].champion.values[0]
        suppPlayer = df[(df['gameid'] == game) & (
            df['side'] == side) & (df['position'] == 'sup')].playername.values[0]
        if (suppPlayer != 'unknown player'):
            supp = int(
                df_champions.loc[df_champions['id'] == supp]['key'])
        else:
            return

        #TIME
        team = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].teamname.values[0]        

        # PRIMEIRO BAN
        ban1 = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].ban1.values[0]        
        if isinstance(ban1, str):
            ban1 = int(df_champions.loc[df_champions['id'] == ban1]['key'])
        else:
            ban1 = ''
            
        # SEGUNDO BAN
        ban2 = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].ban2.values[0]
        if isinstance(ban2, str):
            ban2 = int(df_champions.loc[df_champions['id'] == ban2]['key'])
        else:
            ban2 = ''

        # TERCEIRO BAN
        ban3 = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].ban3.values[0]
        if isinstance(ban3, str):
            ban3 = int(df_champions.loc[df_champions['id'] == ban3]['key'])
        else:
            ban3 = ''

        # QUARTO BAN
        ban4 = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].ban4.values[0]
        if isinstance(ban4, str):
            ban4 = int(df_champions.loc[df_champions['id'] == ban4]['key'])
        else:
            ban4 = ''

        # QUINTO BAN
        ban5 = df[(df['gameid'] == game) & (df['side'] == side)
                   & (df['position'] == 'team')].ban5.values[0]
        
        if isinstance(ban5, str):
            ban5 = int(df_champions.loc[df_champions['id'] == ban5]['key'])
        else:
            ban5 = ''

        # RESULT
        result = df[(df['gameid'] == game) & (df['side'] == side)
                    & (df['position'] == 'team')].result.values[0]

        # STRUCTURES AND BUFFS
        firstBlood = df[(df['gameid'] == game) & (df['side'] == side)
                        & (df['position'] == 'team')].firstblood.values[0]
        firstTower = df[(df['gameid'] == game) & (df['side'] == side)
                        & (df['position'] == 'team')].firsttower.values[0]
        firstHerald = df[(df['gameid'] == game) & (df['side'] == side)
                         & (df['position'] == 'team')].firstherald.values[0]

        if side == 'Blue':
            flagSide = 1
        else:
            flagSide = 0

        # WRITING TO DATASET FILE
        with open('data/clean.csv', mode='a', newline="", encoding='utf-8') as datasetSecondary2022:
            datasetWriter = csv.writer(datasetSecondary2022, delimiter=',')
            datasetWriter.writerow([game, flagSide, team, result, top, jungle, mid, carry, supp, ban1, ban2, ban3, ban4, ban5, firstBlood, firstTower, firstHerald])


df = pd.read_csv("data/raw.csv")
df21 = df.copy()
df_champions = pd.read_csv('data/champions.csv')
games = df21.gameid.drop_duplicates()
sides = ['Blue', 'Red']

header = 'game,flagSide,team,result,top,jungle,mid,carry,supp,ban1,ban2,ban3,ban4,ban5,firstBlood,firstTower,firstHerald\n'
with open('data/clean.csv', mode='a', encoding='utf-8') as dataset:
    dataset.write(header)

for game in games:
    for side in sides:
        processGames(game, side)
