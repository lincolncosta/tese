# MOBA's Oracle: a guideline for esports' win prediction

Geração do dataset

1. Acesse o site https://oracleselixir.com/tools/downloads e baixe o csv com as partidas do ano que será analisado.
2. Salve o arquivo na pasta data com o nome raw.csv.
3. Crie um arquivo crawler-input.csv na pasta data/crawler.
4. Execute o arquivo crawlers/event-crawler-input-cleaner.py. Ele preencherá o arquivo crawler-input.csv.
5. Busque cada uma das partidas do arquivo crawler-input.csv no site https://gol.gg e extraia o identificador delas (ex: o identificador é "44693" em https://gol.gg/game/stats/44693/page-game/), colocando-o na coluna "golId" da partida em questão nesse mesmo arquivo.
6. Crie um arquivo crawler-output.csv
7. Execute o arquivo crawlers/event-dataset-crawler.py Ele preencherá o arquivo crawler-output.csv.
8. Crie um arquivo players_statistics-2023.csv
9. Execute o arquivo crawlers/statistics-dataset-crawler.py Ele preencherá o arquivo players_statistics-2023.csv.
10. Crie um arquivo unified-events-statistics-2023.csv
11. Execute o arquivo crawlers/unify-events-statistics-datasets.py Ele preencherá o arquivo unified-events-statistics-2023.csv.