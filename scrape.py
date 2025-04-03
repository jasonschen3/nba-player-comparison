# Scrapes heights of nba players

import requests
from bs4 import BeautifulSoup
import pandas as pd


url="https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser") # html parser

current_players = set() # Current players this season

# Find all rows in the table body
for row in soup.select("tbody tr"):
    print(row)
    name_cell = row.find("td", {"data-stat": "name_display"})
    if name_cell and name_cell.a:
        player_name = name_cell.a.text.strip()
        current_players.add(player_name)

# Now use the players to scrape the heights and weights
player_data = {}
print(current_players)

# Loop through a-z pages
for letter in "abcdefghijklmnopqrstuvwxyz":
    height_weight_url = f"https://www.basketball-reference.com/players/{letter}/"
    response = requests.get(height_weight_url)
    soup = BeautifulSoup(response.text, "html.parser") # Init soup for each response

    for row in soup.select("tr"):
        header_row = row.select("th")
        player_name = header_row[0].text.strip()
        print("Candidate", player_name)

        if player_name in current_players:
            height_cell = row.find("td", {"data-stat": "height"})
            weight_cell = row.find("td", {"data-stat": "weight"})
            # print(height_cell) # <td class="right" csk="76.0" data-stat="height">6-4</td>

            # .strip() just in case data has whitespace or \n
            player_data[player_name] = {
                "height": height_cell.text.strip(),
                "weight": weight_cell.text.strip(),
            }

print(player_data)
# Export as csv
df = pd.DataFrame.from_dict(player_data, orient="index")
csv_path = 'measurements.csv'
df.to_csv(csv_path)

print(f"Data exported to {csv_path}")


    


