import pandas as pd
from tqdm import tqdm
import csv

df = pd.read_csv('../data/crawler/unified-events-statistics.csv')
ordem_colunas = ['BLUE:first_blood',
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

pontuacao_dict = {
    'first_blood': 300,
    'dragon': 500,
    'herald': 350,
    'first_tower_top': 250,
    'first_tower_mid': 250,
    'first_tower_bot': 250,
    'second_tower_top': 400,
    'second_tower_mid': 400,
    'second_tower_bot': 400,
    'third_tower_top': 500,
    'third_tower_mid': 500,
    'third_tower_bot': 500,    
    'inhibitor_top': 500,
    'inhibitor_mid': 500,
    'inhibitor_bot': 500,
    'baron': 500,
    'elder_dragon': 500,
    'nexus_tower': 500,
    'nexus': 1000
}

def calcula_pontuacao_time(pontuacao_atual, evento):
     return int(pontuacao_atual) + int(pontuacao_dict.get(evento))


for index, row in tqdm(df.iterrows(), total=len(df)):
  
    result = row['result']
    
    # Busca os eventos da partida a cada 1 minuto até os 60 minutos
    for time_considered in range(0, 61, 1):
        eventos = []
        contagem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        duracao_min = row['duracao_min']
        redPontuacaoObjetivos = 0
        bluePontuacaoObjetivos = 0

        # Se a partida já estiver finalizada nessa iteração, vai para a próxima partida
        if time_considered > duracao_min:
                break

        for i in range(1, 46):
            evento = f'event{i}'
            tempo = f'event{i}time'

            # Verificar se o evento aconteceu antes de "time_considered" minutos
            if pd.notna(row[tempo]) and row[tempo] <= time_considered:
                if 'RED' in row[evento]:
                    redPontuacaoObjetivos = calcula_pontuacao_time(redPontuacaoObjetivos, row[evento].replace(' ', '').split(':')[1])
                else:
                    bluePontuacaoObjetivos = calcula_pontuacao_time(bluePontuacaoObjetivos, row[evento].replace(' ', '').split(':')[1]) 
                
                eventos.append(row[evento].replace(' ', ''))

                # Criar um DataFrame com base na lista de colunas
                df_contagem = pd.DataFrame({'coluna': eventos})

                # Contar as ocorrências de cada coluna
                contagem = df_contagem['coluna'].value_counts().reindex(ordem_colunas)
                contagem = contagem.fillna(0).astype(int).to_list()

        golId = row['golId']
        time = time_considered        
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
        
        features = [golId,time,result,blueTopGP,blueTopWR,blueTopKDA,blueJungleGP,blueJungleWR,blueJungleKDA,blueMidGP,blueMidWR,blueMidKDA,blueADCGP,blueADCWR,blueADCKDA,blueSupportGP,blueSupportWR,blueSupportKDA,bluePontuacaoObjetivos,redTopGP,redTopWR,redTopKDA,redJungleGP,redJungleWR,redJungleKDA,redMidGP,redMidWR,redMidKDA,redAdcGP,redAdcWR,redAdcKDA,redSupportGP,redSupportWR,redSupportKDA, redPontuacaoObjetivos]
        features.extend(contagem)

        with open('../data/crawler/unified-events-time-statistics.csv', mode='a', newline="") as dataset:            
            datasetWriter = csv.writer(dataset, delimiter=',')
            datasetWriter.writerow(features)