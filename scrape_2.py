from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrapes and bypasses rate limiter
url="https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"

driver = webdriver.Firefox()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html)

current_players = set() # Current players this season

# Find all rows in the table body
for row in soup.select("tbody tr"):
    print(row)
    name_cell = row.find("td", {"data-stat": "name_display"})
    if name_cell and name_cell.a:
        player_name = name_cell.a.text.strip()
        current_players.add(player_name)

print(current_players)

# Now use the players to scrape the heights and weights
player_data = {}

# Loop through a-z pages
for letter in "abcdefghijklmnopqrstuvwxyz":
    height_weight_url = f"https://www.basketball-reference.com/players/{letter}/"
    response = requests.get(height_weight_url)
    soup = BeautifulSoup(response.text, "html.parser")

    for row in soup.select("tr"):
        header_row = row.select("th")
        player_name = header_row[0].text.strip()
        print("Candidate", player_name)

        if player_name in current_players:
            height_cell = row.find("td", {"data-stat": "height"})
            weight_cell = row.find("td", {"data-stat": "weight"})
            
            player_data[player_name] = {
                "height": height_cell.text.strip(),
                "weight": weight_cell.text.strip(),
            }

# Export as csv
df = pd.DataFrame.from_dict(player_data, orient="index")
csv_path = 'measurements.csv'
df.to_csv(csv_path)

print(f"Data exported to {csv_path}")


    


