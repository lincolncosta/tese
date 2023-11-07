import pandas as pd
import threading
import csv

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service

df = pd.read_csv("../data/crawler/crawler-input.csv")
games = df.golId.drop_duplicates().dropna().apply(int).tolist()
processed_df = pd.read_csv("../data/crawler/crawler-output-with-kills.csv")
processed_games = processed_df.golId.drop_duplicates().tolist()
remaining_games = set(games) - set(processed_games)

def getFormattedAction(img_src):
    actionMapping = {
        'https://gol.gg/_img/kill-icon.png': 'first_blood',
        'https://gol.gg/_img/drake-icon.png': 'dragon',
        'https://gol.gg/_img/chemtech-dragon.png': 'dragon',
        'https://gol.gg/_img/hextech-dragon.png': 'dragon',
        'https://gol.gg/_img/mountain-dragon.png': 'dragon',
        'https://gol.gg/_img/cloud-dragon.png': 'dragon',
        'https://gol.gg/_img/ocean-dragon.png': 'dragon',
        'https://gol.gg/_img/fire-dragon.png': 'dragon',
        'https://gol.gg/_img/elder-dragon.png': 'elder_dragon',
        'https://gol.gg/_img/nashor-icon.png': 'baron',
        'https://gol.gg/_img/herald-icon.png': 'herald',
        'https://gol.gg/_img/nexus-icon.png': 'nexus',
        'https://gol.gg/_img/inhib-icon.png': 'need_target',
        'https://gol.gg/_img/tower-icon.png': 'need_target',
    }

    if img_src in actionMapping:
        return actionMapping[img_src]
    else:
        return img_src

def getFormattedTarget(target_text):
    targetMapping = {
        'T1 TOP': 'first_tower_top',
        'T1 MID': 'first_tower_mid',
        'T1 BOT': 'first_tower_bot',
        'T2 TOP': 'second_tower_top',
        'T2 MID': 'second_tower_mid',
        'T2 BOT': 'second_tower_bot',
        'T3 TOP': 'third_tower_top',
        'T3 MID': 'third_tower_mid',
        'T3 BOT': 'third_tower_bot',
        'INHIB TOP': 'inhibitor_top',
        'INHIB MID': 'inhibitor_mid',
        'INHIB BOT': 'inhibitor_bot',
        'T2 BOT NEXUS': 'nexus_tower',
        'T1 TOP NEXUS': 'nexus_tower',
    }

    if target_text in targetMapping:
        return targetMapping[target_text]
    else:
        return target_text

def processGames(game):
    
    if game != 'nan':
        game = str(game)
        chrome_path = r'../dependency/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('window-size=1400,600')
        options.add_argument(f'user-agent={user_agent}')
        service = Service(executable_path=chrome_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(
            "https://gol.gg/game/stats/{}/page-timeline/".format(game))

        # waiting page load
        msg = 'Tabela de eventos era esperada na partida {} e não foi encontrado.'.format(game)
        wait = WebDriverWait(driver, 10)
        events_table = wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'timeline')), message=msg)        
        rows = events_table.find_elements(By.TAG_NAME, "tr")
        events = [game, '', '', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '','','','','','','','','','','','','', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '', '', '', '','', '', '', '', '', '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','', '', '', '','', '', '', '', '', '','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
        event_counter = 1
        has_first_blood = False

        for index, row in enumerate(rows):
            # skipping first row (header)
            if index == 0:
                continue

            time = row.find_elements(By.TAG_NAME, "td")[0]
            side = row.find_elements(By.TAG_NAME, "td")[1]
            side_img = side.find_elements(By.CLASS_NAME, "champion_icon_light")[0]
            action = row.find_elements(By.TAG_NAME, "td")[4]
            action_img = action.find_elements(By.CLASS_NAME, "champion_icon_light")

            # skipping empty actions
            # if (len(action_img)) == 0:
            #     continue
            
            target = row.find_elements(By.TAG_NAME, "td")[6]

            result_str = ''

            if('blue' in side_img.get_attribute("src")):
                result_str += 'BLUE: '
            else:
                result_str += 'RED: '

            if action.text == 'PLATE':
                result_str += 'plate'
                events[event_counter] = result_str
                events[event_counter + 200] = time.text.split(':')[0]
                event_counter += 1
                has_first_blood = True
                continue
            else:
                action_img = action_img[0]
                formatted_action = getFormattedAction(action_img.get_attribute("src"))

            if(formatted_action == 'first_blood'):                                
                if has_first_blood:
                    result_str += 'kill'
                else:
                    result_str += 'first_blood'
                events[event_counter] = result_str
                events[event_counter + 200] = time.text.split(':')[0]
                event_counter += 1
                has_first_blood = True
                continue

            if(formatted_action != 'need_target'):
                result_str += formatted_action
            else:
                formatted_target = getFormattedTarget(target.text)
                result_str += formatted_target

            events[event_counter] = result_str
            events[event_counter + 200] = time.text.split(':')[0]
            event_counter += 1

        with open('../data/crawler/crawler-output-with-kills.csv', mode='a', newline="") as dataset:
            datasetWriter = csv.writer(dataset, delimiter=',')
            datasetWriter.writerow(events)
            
semaphore = threading.Semaphore(4)

def thread_func():
    while True:
        # Obtém um item do conjunto com o semáforo
        with semaphore:
            if not remaining_games:
                break
            game = remaining_games.pop()
        # Executa o crawler para o item
        processGames(game)

# Cria e inicia quatro threads
threads = [threading.Thread(target=thread_func) for _ in range(6)]

for thread in threads:
    thread.start()

# Espera todas as threads terminarem
for thread in threads:
    thread.join()

print("Todas as threads terminaram.")

#for game in tqdm(remaining_games):
#    game = int(game)
#    processGames(game)