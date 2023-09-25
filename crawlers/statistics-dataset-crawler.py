import pandas as pd
import numpy as np

import csv
import time
import threading

from tqdm import tqdm
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from concurrent.futures import ThreadPoolExecutor

def getPlayerPerformance(playerName, playerChampion, formatedStartDate, formatedEndDate, position):
        filtered_df = df[(df['playername'] == playerName) & (df['champion'] == playerChampion) & (df['position'] == position) & (df['date'] >= formatedStartDate) & (df['date'] <= formatedEndDate)]        

        gp = len(filtered_df.index)
        kda = 0
        wr = 0

        if (gp != 0):
            kills_sum = filtered_df['kills'].sum()
            deaths_sum = filtered_df['deaths'].sum()
            assists_sum = filtered_df['assists'].sum()

            games_won_red = filtered_df[(filtered_df['result'] == 0) & (filtered_df['side'] == 'Red')]
            games_won_blue = filtered_df[(filtered_df['result'] == 1) & (filtered_df['side'] == 'Blue')]

            frames = [games_won_red, games_won_blue]
            games_won = pd.concat(frames)

            if deaths_sum != 0:
                kda = round(((kills_sum + assists_sum)/ deaths_sum), 2)
            else:
                kda = kills_sum + assists_sum
            wr = round(len(games_won.index) / gp, 2)

        return gp, wr, kda

def processGames(game):
    
    # GAME DATETIME
    endDate = dt.strptime(
        df[(df['gameid'] == game)].date.values[0], '%Y-%m-%d %H:%M:%S')
    startDate = endDate - relativedelta(months=6)    
    formatedEndDate = "{}-{:02d}-{:02d}".format(
        endDate.year, endDate.month, endDate.day - 1)
    formatedStartDate = ''    
    formatedStartDate = "{}-{:02d}-{:02d}".format(startDate.year, startDate.month, startDate.day - 1)

    # BLUE TEAM
    blueTop = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                    & (df['position'] == 'top')].champion.values[0]
    blueTopPlayer = df[(df['gameid'] == game) & (df['side'] == 'Blue') & (
        df['position'] == 'top')].playername.values[0]
    if (blueTopPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            blueTopPlayer, blueTop, formatedStartDate, formatedEndDate, 'top')
        blueTop = int(
            df_champions.loc[df_champions['id'] == blueTop]['key'])
        if (crawler):
            blueTopGP = crawler[0]
            blueTopWR = crawler[1]
            blueTopKDA = crawler[2]
        else:
            return
    else:
        return

    blueJungle = df[(df['gameid'] == game) & (df['side'] == 'Blue') & (
        df['position'] == 'jng')].champion.values[0]
    blueJunglePlayer = df[(df['gameid'] == game) & (
        df['side'] == 'Blue') & (df['position'] == 'jng')].playername.values[0]
    if (blueJunglePlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            blueJunglePlayer, blueJungle, formatedStartDate, formatedEndDate, 'jng')
        blueJungle = int(
            df_champions.loc[df_champions['id'] == blueJungle]['key'])
        if (crawler):
            blueJungleGP = crawler[0]
            blueJungleWR = crawler[1]
            blueJungleKDA = crawler[2]
        else:
            return
    else:
        return

    blueMid = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                    & (df['position'] == 'mid')].champion.values[0]
    blueMidPlayer = df[(df['gameid'] == game) & (df['side'] == 'Blue') & (
        df['position'] == 'mid')].playername.values[0]
    if (blueMidPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            blueMidPlayer, blueMid, formatedStartDate, formatedEndDate, 'mid')
        blueMid = int(
            df_champions.loc[df_champions['id'] == blueMid]['key'])
        if (crawler):
            blueMidGP = crawler[0]
            blueMidWR = crawler[1]
            blueMidKDA = crawler[2]
        else:
            return
    else:
        return

    blueCarry = df[(df['gameid'] == game) & (df['side'] == 'Blue') & (
        df['position'] == 'bot')].champion.values[0]
    blueCarryPlayer = df[(df['gameid'] == game) & (
        df['side'] == 'Blue') & (df['position'] == 'bot')].playername.values[0]
    if (blueCarryPlayer != 'unknown player' and blueCarryPlayer != 'Deadly'):
        crawler = getPlayerPerformance(
            blueCarryPlayer, blueCarry, formatedStartDate, formatedEndDate, 'bot')
        blueCarry = int(
            df_champions.loc[df_champions['id'] == blueCarry]['key'])
        if (crawler):
            blueCarryGP = crawler[0]
            blueCarryWR = crawler[1]
            blueCarryKDA = crawler[2]
        else:
            return
    else:
        return

    blueSupp = df[(df['gameid'] == game) & (df['side'] == 'Blue') & (
        df['position'] == 'sup')].champion.values[0]
    blueSuppPlayer = df[(df['gameid'] == game) & (
        df['side'] == 'Blue') & (df['position'] == 'sup')].playername.values[0]
    if (blueSuppPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            blueSuppPlayer, blueSupp, formatedStartDate, formatedEndDate, 'sup')
        blueSupp = int(
            df_champions.loc[df_champions['id'] == blueSupp]['key'])
        if (crawler):
            blueSuppGP = crawler[0]
            blueSuppWR = crawler[1]
            blueSuppKDA = crawler[2]
        else:
            return
    else:
        return

    # RED TEAM
    redTop = df[(df['gameid'] == game) & (df['side'] == 'Red')
                & (df['position'] == 'top')].champion.values[0]
    redTopPlayer = df[(df['gameid'] == game) & (df['side'] == 'Red') & (
        df['position'] == 'top')].playername.values[0]
    if (redTopPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            redTopPlayer, redTop, formatedStartDate, formatedEndDate, 'top')
        redTop = int(df_champions.loc[df_champions['id'] == redTop]['key'])
        if (crawler):
            redTopGP = crawler[0]
            redTopWR = crawler[1]
            redTopKDA = crawler[2]
        else:
            return
    else:
        return

    redJungle = df[(df['gameid'] == game) & (df['side'] == 'Red') & (
        df['position'] == 'jng')].champion.values[0]
    redJunglePlayer = df[(df['gameid'] == game) & (
        df['side'] == 'Red') & (df['position'] == 'jng')].playername.values[0]
    if (redJunglePlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            redJunglePlayer, redJungle, formatedStartDate, formatedEndDate, 'jng')
        redJungle = int(
            df_champions.loc[df_champions['id'] == redJungle]['key'])
        if (crawler):
            redJungleGP = crawler[0]
            redJungleWR = crawler[1]
            redJungleKDA = crawler[2]
        else:
            return
    else:
        return

    redMid = df[(df['gameid'] == game) & (df['side'] == 'Red')
                & (df['position'] == 'mid')].champion.values[0]
    redMidPlayer = df[(df['gameid'] == game) & (df['side'] == 'Red') & (
        df['position'] == 'mid')].playername.values[0]
    if (redMidPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            redMidPlayer, redMid, formatedStartDate, formatedEndDate, 'mid')
        redMid = int(df_champions.loc[df_champions['id'] == redMid]['key'])
        if (crawler):
            redMidGP = crawler[0]
            redMidWR = crawler[1]
            redMidKDA = crawler[2]
        else:
            return
    else:
        return

    redCarry = df[(df['gameid'] == game) & (df['side'] == 'Red') & (
        df['position'] == 'bot')].champion.values[0]
    redCarryPlayer = df[(df['gameid'] == game) & (
        df['side'] == 'Red') & (df['position'] == 'bot')].playername.values[0]
    if (redCarryPlayer != 'unknown player' and blueCarryPlayer != 'Deadly'):
        crawler = getPlayerPerformance(
            redCarryPlayer, redCarry, formatedStartDate, formatedEndDate, 'bot')
        redCarry = int(
            df_champions.loc[df_champions['id'] == redCarry]['key'])
        if (crawler):
            redCarryGP = crawler[0]
            redCarryWR = crawler[1]
            redCarryKDA = crawler[2]
        else:
            return
    else:
        return

    redSupp = df[(df['gameid'] == game) & (df['side'] == 'Red')
                    & (df['position'] == 'sup')].champion.values[0]
    redSuppPlayer = df[(df['gameid'] == game) & (df['side'] == 'Red') & (
        df['position'] == 'sup')].playername.values[0]
    if (redSuppPlayer != 'unknown player'):
        crawler = getPlayerPerformance(
            redSuppPlayer, redSupp, formatedStartDate, formatedEndDate, 'sup')
        redSupp = int(
            df_champions.loc[df_champions['id'] == redSupp]['key'])
        if (crawler):
            redSuppGP = crawler[0]
            redSuppWR = crawler[1]
            redSuppKDA = crawler[2]
        else:
            return
    else:
        return

    # RESULT
    result = df[(df['gameid'] == game) & (df['side'] == 'Blue')
                & (df['position'] == 'sup')].result.values[0]

    # WRITING TO DATASET FILE
    with open('../data/crawler/players_statistics-2023.csv', mode='a', newline="") as dataset2021:
        datasetWriter = csv.writer(dataset2021, delimiter=',')
        datasetWriter.writerow([game, blueTopGP, blueTopWR, blueTopKDA, blueJungleGP, blueJungleWR, blueJungleKDA, blueMidGP, blueMidWR, blueMidKDA, blueCarryGP, blueCarryWR, blueCarryKDA, blueSuppGP, blueSuppWR,
                                blueSuppKDA, redTopGP, redTopWR, redTopKDA, redJungleGP, redJungleWR, redJungleKDA, redMidGP, redMidWR, redMidKDA, redCarryGP, redCarryWR, redCarryKDA, redSuppGP, redSuppWR, redSuppKDA, result])

def diff(list1, list2):
    c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
    d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
    return list(c - d)

df = pd.read_csv("../data/raw-2023.csv")
df_champions = pd.read_csv('../data/champions.csv')
statistics_df = pd.read_csv("../data/crawler/players_statistics-2023.csv")
events_output_df = pd.read_csv("../data/crawler/crawler-output-2023.csv")
events_input_df = pd.read_csv("../data/crawler/crawler-input-2023.csv")

processedGameIds = statistics_df.game.drop_duplicates().to_list()
unprocessedGameIds = []

for index, row in events_output_df.iterrows():
    golId = row['golId']

    if np.isfinite(golId):
        filtered_df = events_input_df.loc[events_input_df['golId'] == golId]
        game = filtered_df['game'].values[0]
        unprocessedGameIds.append(game)

gamesToProcess = diff(processedGameIds, unprocessedGameIds)

header = 'game,blueTopGP,blueTopWR,blueTopKDA,blueJungleGP,blueJungleWR,blueJungleKDA,blueMidGP,blueMidWR,blueMidKDA,blueADCGP,blueADCWR,blueADCKDA,blueSupportGP,blueSupportWR,blueSupportKDA,redTopGP,redTopWR,redTopKDA,redJungleGP,redJungleWR,redJungleKDA,redMidGP,redMidWR,redMidKDA,redAdcGP,redAdcWR,redAdcKDA,redSupportGP,redSupportWR,redSupportKDA,result\n'
with open('../data/crawler/players_statistics-2023.csv', mode='a') as dataset:
    dataset.write(header)

for game in tqdm(gamesToProcess):
    if isinstance(game, str):
        processGames(game)