import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.offline as py
from sklearn.decomposition import PCA

df = pd.read_csv("data/crawler/unified-events-statistics-with-kills.csv")

def formata_evento(evento):
    # Dicionário para mapear times
    times = {
        "BLUE": "Blue team",
        "RED": "Red team"
    }

    # Dicionário para mapear eventos
    eventos = {
        "first_blood": "got first blood",
        "plate": "got a tower plate",
        "kill": "killed an enemy",
        "dragon": "got dragon",
        "voidgrub": "got voidgrub",
        "herald": "got herald",
        "first_tower_top": "destroyed the first top tower",
        "first_tower_mid": "destroyed the first mid tower",
        "first_tower_bot": "destroyed the first bot tower",
        "second_tower_top": "destroyed the second top tower",
        "second_tower_mid": "destroyed the second mid tower",
        "second_tower_bot": "destroyed the second bot tower",
        "third_tower_top": "destroyed the third top tower",
        "third_tower_mid": "destroyed the third mid tower",
        "third_tower_bot": "destroyed the third bot tower",
        "inhibitor_top": "destroyed the top inhibitor",
        "inhibitor_mid": "destroyed the mid inhibitor",
        "inhibitor_bot": "destroyed the bot inhibitor",
        "baron": "got Baron",
        "elder_dragon": "got Elder Dragon",
        "nexus_tower": "destroyed a Nexus tower",
        "nexus": "destroyed the Nexus"
    }

    # Separar o time e o evento
    time, acao = evento.split(": ")
    
    # Construir a string interpretada
    interpretacao = f"{times[time]} {eventos[acao]}"
    
    return interpretacao

# Inicializa uma lista para armazenar as descrições dos eventos
event_descriptions = []

# Itera sobre cada golId único
for golId in df['golId'].unique():
    # Filtra o DataFrame para a partida atual
    partida_df = df[df['golId'] == golId]
    
    event_descriptions.append((golId, f"Blue team top laner has selected {partida_df.iloc[0]['blueTopChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['blueTopGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['blueTopKDA']} and a win rate of {partida_df.iloc[0]['blueTopWR']}."))
    event_descriptions.append((golId, f"Blue team jungler has selected {partida_df.iloc[0]['blueJungleChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['blueJungleGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['blueJungleKDA']} and a win rate of {partida_df.iloc[0]['blueJungleWR']}."))
    event_descriptions.append((golId, f"Blue team mid laner has selected {partida_df.iloc[0]['blueMidChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['blueMidGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['blueMidKDA']} and a win rate of {partida_df.iloc[0]['blueMidWR']}."))
    event_descriptions.append((golId, f"Blue team ad carry has selected {partida_df.iloc[0]['blueADCChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['blueADCGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['blueADCKDA']} and a win rate of {partida_df.iloc[0]['blueADCWR']}."))
    event_descriptions.append((golId, f"Blue team support has selected {partida_df.iloc[0]['blueSupportChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['blueSupportGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['blueSupportKDA']} and a win rate of {partida_df.iloc[0]['blueSupportWR']}."))

    event_descriptions.append((golId, f"Red team top laner has selected {partida_df.iloc[0]['redTopChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['redTopGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['redTopKDA']} and a win rate of {partida_df.iloc[0]['redTopWR']}."))
    event_descriptions.append((golId, f"Red team jungler has selected {partida_df.iloc[0]['redJungleChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['redJungleGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['redJungleKDA']} and a win rate of {partida_df.iloc[0]['redJungleWR']}."))
    event_descriptions.append((golId, f"Red team mid laner has selected {partida_df.iloc[0]['redMidChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['redMidGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['redMidKDA']} and a win rate of {partida_df.iloc[0]['redMidWR']}."))
    event_descriptions.append((golId, f"Red team ad carry has selected {partida_df.iloc[0]['redAdcChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['redAdcGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['redAdcKDA']} and a win rate of {partida_df.iloc[0]['redAdcWR']}."))
    event_descriptions.append((golId, f"Red team support has selected {partida_df.iloc[0]['redSupportChampion']}. Over the last 6 months, he has played {partida_df.iloc[0]['redSupportGP']} matches with this champion, having a KDA of {partida_df.iloc[0]['redSupportKDA']} and a win rate of {partida_df.iloc[0]['redSupportWR']}."))

    # Itera sobre cada evento (eventX) da partida atual
    for evento in range(1, 201):  # Assumindo que eventX varia de 1 a 200
        evento_col = f"event{evento}"
        tempo_col = f"event{evento}time"
        
        # Filtra eventos não nulos para a partida e evento atual
        eventos_validos = partida_df[(partida_df[evento_col].notnull()) & (partida_df[tempo_col].notnull())]
        
        # Itera sobre os eventos válidos e cria a descrição do evento
        for index, row in eventos_validos.iterrows():
            event_name = row[evento_col]
            event_time = row[tempo_col]
            event_description = f"Event {evento}: {formata_evento(event_name)} happened at minute {event_time}."
            event_descriptions.append((golId, event_description, event_time, partida_df.iloc[0]['redSupportKDA']))
    

# Converte a lista de descrições dos eventos para um DataFrame
event_df = pd.DataFrame(event_descriptions, columns=["match_id", "event_description", "event_time", "result"])

# Salva o DataFrame resultante em um arquivo CSV
event_df.to_csv("chat-gpt-2024.csv", index=False)