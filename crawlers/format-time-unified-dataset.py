import pandas as pd
import numpy as np

def qtd_eventos(integer):
    qtdNulos = integer / 2
    return int(45 - qtdNulos)

df = pd.read_csv('../data/crawler/unified-events-statistics.csv')

# Formatando colunas
qtd_eventos = list(map(qtd_eventos, df.isnull().sum(axis=1).tolist()))
df['qtd_eventos'] = qtd_eventos

for index, row in df.iterrows():
    qtdEventos = row['qtd_eventos']
    duracao = row['event{}time'.format(qtdEventos)]    
    df.at[index, 'duracao_min'] = int(duracao.split(':')[0])

    for i in range(1, 46):
        if isinstance(row['event{}time'.format(i)], str):
            df.at[index, 'event{}time'.format(i)] = int(row['event{}time'.format(i)].split(':')[0])
    

df = df.astype({'duracao_min':'int'})
convert_dict = {'event1time': 'Int64','event2time': 'Int64','event3time': 'Int64','event4time': 'Int64','event5time': 'Int64','event6time': 'Int64','event7time': 'Int64','event8time': 'Int64','event9time': 'Int64','event10time': 'Int64','event11time': 'Int64','event12time': 'Int64','event13time': 'Int64','event14time': 'Int64','event15time': 'Int64','event16time': 'Int64','event17time': 'Int64','event18time': 'Int64','event19time': 'Int64','event20time': 'Int64','event21time': 'Int64','event22time': 'Int64','event23time': 'Int64','event24time': 'Int64','event25time': 'Int64','event26time': 'Int64','event27time': 'Int64','event28time': 'Int64','event29time': 'Int64','event30time': 'Int64','event31time': 'Int64','event32time': 'Int64','event33time': 'Int64','event34time': 'Int64','event35time': 'Int64','event36time': 'Int64','event37time': 'Int64','event38time': 'Int64','event39time': 'Int64','event40time': 'Int64','event41time': 'Int64','event42time': 'Int64','event43time': 'Int64','event44time': 'Int64','event45time': 'Int64'} 
df = df.astype(convert_dict, errors='ignore')


df.to_csv('../data/crawler/unified-events-statistics.csv', index=False)