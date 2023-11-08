import pandas as pd
from tqdm import tqdm
import csv

df = pd.read_csv('../data/crawler/unified-events-statistics-with-kills.csv')
df = df.fillna(0)
ordem_colunas = [
    'BLUE:kill',
    'BLUE:plate'
    'BLUE:first_blood',
    'BLUE:dragon',
    'BLUE:herald',
    'BLUE:first_tower_top',
    'BLUE:first_tower_mid',
    'BLUE:first_tower_bot',
    'BLUE:second_tower_top',
    'BLUE:second_tower_mid',
    'BLUE:second_tower_bot',
    'BLUE:third_tower_top',
    'BLUE:third_tower_mid',
    'BLUE:third_tower_bot',
    'BLUE:inhibitor_top',
    'BLUE:inhibitor_mid',
    'BLUE:inhibitor_bot',
    'BLUE:baron',
    'BLUE:elder_dragon',
    'BLUE:nexus_tower',
    'BLUE:nexus',
    'RED:kill',
    'RED:plate',
    'RED:first_blood',
    'RED:dragon',
    'RED:herald',
    'RED:first_tower_top',
    'RED:first_tower_mid',
    'RED:first_tower_bot',
    'RED:second_tower_top',
    'RED:second_tower_mid',
    'RED:second_tower_bot',
    'RED:third_tower_top',
    'RED:third_tower_mid',
    'RED:third_tower_bot',
    'RED:inhibitor_top',
    'RED:inhibitor_mid',
    'RED:inhibitor_bot',
    'RED:baron',
    'RED:elder_dragon',
    'RED:nexus_tower',
    'RED:nexus']

early_start = 0
early_end = 10

mid_start = 11
mid_end = 20

late_start = 21
late_end = 90


for index, row in tqdm(df.iterrows(), total=len(df)):
  
    result = row['result']
    
    eventos = []
    contagem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]    

    for i in range(1, 200):
        evento = f'event{i}'
        tempo = f'event{i}time'

        if pd.notna(row[tempo]) and row[tempo] >= mid_start and row[tempo] <= mid_end: 
            if(row[evento] != 0):
                eventos.append(row[evento].replace(' ', ''))

            # Criar um DataFrame com base na lista de colunas
            df_contagem = pd.DataFrame({'coluna': eventos})

            # Contar as ocorrências de cada coluna
            contagem = df_contagem['coluna'].value_counts().reindex(ordem_colunas)
            contagem = contagem.fillna(0).astype(int).to_list()

    golId = row['golId']
    blueTopGP = row['blueTopGP']
    blueTopWR = row['blueTopWR']
    blueTopKDA = row['blueTopKDA']
    blueJungleGP = row['blueJungleGP']
    blueJungleWR = row['blueJungleWR']
    blueJungleKDA = row['blueJungleKDA']
    blueMidGP = row['blueMidGP']
    blueMidWR = row['blueMidWR']
    blueMidKDA = row['blueMidKDA']
    blueADCGP = row['blueADCGP']
    blueADCWR = row['blueADCWR']
    blueADCKDA = row['blueADCKDA']
    blueSupportGP = row['blueSupportGP']
    blueSupportWR = row['blueSupportWR']
    blueSupportKDA = row['blueSupportKDA']
    redTopGP = row['redTopGP']
    redTopWR = row['redTopWR']
    redTopKDA = row['redTopKDA']
    redJungleGP = row['redJungleGP']
    redJungleWR = row['redJungleWR']
    redJungleKDA = row['redJungleKDA']
    redMidGP = row['redMidGP']
    redMidWR = row['redMidWR']
    redMidKDA = row['redMidKDA']
    redAdcGP = row['redAdcGP']
    redAdcWR = row['redAdcWR']
    redAdcKDA = row['redAdcKDA']
    redSupportGP = row['redSupportGP']
    redSupportWR = row['redSupportWR']
    redSupportKDA = row['redSupportKDA']
    
    features = [golId,result,blueTopGP,blueTopWR,blueTopKDA,blueJungleGP,blueJungleWR,blueJungleKDA,blueMidGP,blueMidWR,blueMidKDA,blueADCGP,blueADCWR,blueADCKDA,blueSupportGP,blueSupportWR,blueSupportKDA,redTopGP,redTopWR,redTopKDA,redJungleGP,redJungleWR,redJungleKDA,redMidGP,redMidWR,redMidKDA,redAdcGP,redAdcWR,redAdcKDA,redSupportGP,redSupportWR,redSupportKDA]
    features.extend(contagem)

    with open('../data/crawler/unified-events-statistics-with-kills-as-columns-mid.csv', mode='a', newline="") as dataset:            
        datasetWriter = csv.writer(dataset, delimiter=',')
        datasetWriter.writerow(features)