## Data Collection
For data collection, we scrapped the user replay data from the top 500 Pokémon showdown gamers (both OU and random battle). We used Selenium and Pandas (Beautiful Soup) to scrape the data from these sites and stored it in an SQLite database. 
The ladder consists of data of the top 500 players of Pokémon showdown for various types of game battles. After getting the top players, we navigated to the replays site to scrap the replay data of all users. The log is in text format. There are keywords( like a switch, move, damage, etc) which represent the gameplay data.

We also scrapped the data from Babiri website to find the top 10 Pokémon used by players. 
This would help us in forming the Pokémon teams if required.

 ## Files in Data Collection
 
 Scraping for Babiri Website - babiri_parser.py
 
 Scraping for Pokémon Showdown Replays Website - scrapping_replays_showndown.py
 
 Parsing logic for Human Replays Data - parsing_human_replays_data.py
 
 Parsing Logic for Winning Prediction - parsing_winning_prediction.py
 
 The logic for accessing SQL Lite database - database.py
  
 Sample JSON after parsing for Human Replays Data - sample_parsing_data.json
 
 Google drive link for data files: https://drive.google.com/drive/folders/1tu7qDDw8NLILY4DnVYujWGTD0fcOlu4a?usp=sharing
  
 CSV files used for winning prediction - wins.csv, completed.csv, forfeited.csv
 
 SQL Lite Database : database_for_scrapping.db 
 
 JSON after parsing for Human Replays Data - human_replays_data.json

 
 
 Basic Scrapping idea was taken from https://github.com/vasumv/pokemon_ai/tree/master/log_scraper 

 Scrapped top 100 teams from https://www.babiri.net/#/ 
 
 ## Running the Scrapping Script
 
 To run the script python scrapping_replays_showndown.py with db_path as an argument.
 
 Eg : 
 
 ``` python3 scrapping_replays_showndown.py  db_path: database_for_scrapping.db ```

 
 
