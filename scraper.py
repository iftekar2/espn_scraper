import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import csv
import re
from datetime import datetime

# Database imports
from simple_db_helpers import (
    insert_live_game,
    move_game_to_final,
    create_game_data_dict
)


# --- SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.espn.com/nfl/scoreboard/_/week/7/year/2025/seasontype/2")
time.sleep(5)

# --- CSV SETUP ---
final_headers = [
    "Team_one_logo","team_one_name","team_one_score","team_one_records","team_two_logo","team_two_name","team_two_score","team_two_records",
    "team_one_passing_yard_player_image","team_one_passing_yard_player_name","team_one_passing_yard_player_position","team_one_passing_yard_player_game_state","team_one_player_one_passing_yard",
    "team_two_passing_yard_player_image","team_two_passing_yard_player_name","team_two_passing_yard_player_position","team_two_passing_yard_player_game_state","team_two_player_two_passing_yard",
    "team_one_rushing_yard_player_image","team_one_rushing_yard_player_name","team_one_rushing_yard_player_position","team_one_rushing_yard_player_game_state","team_one_player_one_rushing_yard",
    "team_two_rushing_yard_player_image","team_two_rushing_yard_player_name","team_two_rushing_yard_player_position","team_two_rushing_yard_player_game_state","team_two_player_two_rushing_yard",
    "team_one_receiving_yard_player_image","team_one_receiving_yard_player_name","team_one_receiving_yard_player_position","team_one_receiving_yard_player_game_state","team_one_player_one_receiving_yard",
    "team_two_receiving_yard_player_image","team_two_receiving_yard_player_name","team_two_receiving_yard_player_position","team_two_receiving_yard_player_game_state","team_two_player_two_receiving_yard",
    "team_one_sacks_player_image","team_one_sacks_player_name","team_one_sacks_player_position","team_one_player_one_sacks","team_two_sacks_player_image","team_two_sacks_player_name","team_two_sacks_player_position","team_two_player_two_sacks",
    "team_one_tackles_player_image","team_one_tackles_player_name","team_one_tackles_player_position","team_one_tackles_player_game_state","team_one_player_one_tackles","team_two_tackles_player_image","team_two_tackles_player_name","team_two_tackles_player_position","team_two_tackles_player_game_state","team_two_player_two_tackles",
    "team_one_total_yards","team_two_total_yards","team_one_total_turnovers","team_two_total_turnovers","team_one_first_downs","team_two_first_downs","team_one_penalties","team_two_penalties","team_one_third_down","team_two_third_down","team_one_forth_down","team_two_forth_down","team_one_red_zone","team_two_red_zone","team_one_possession","team_two_possession"
]

# Open the CSV file and write the headers
final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
final_csv_writer = csv.writer(final_csv_file)
final_csv_writer.writerow(final_headers)

live_headers = [
    "Team_one_logo","team_one_name","team_one_score","team_one_records","team_two_logo","team_two_name","team_two_score","team_two_records",
    "team_one_passing_yard_player_image","team_one_passing_yard_player_name","team_one_passing_yard_player_position","team_one_passing_yard_player_game_state","team_one_player_one_passing_yard",
    "team_two_passing_yard_player_image","team_two_passing_yard_player_name","team_two_passing_yard_player_position","team_two_passing_yard_player_game_state","team_two_player_two_passing_yard",
    "team_one_rushing_yard_player_image","team_one_rushing_yard_player_name","team_one_rushing_yard_player_position","team_one_rushing_yard_player_game_state","team_one_player_one_rushing_yard",
    "team_two_rushing_yard_player_image","team_two_rushing_yard_player_name","team_two_rushing_yard_player_position","team_two_rushing_yard_player_game_state","team_two_player_two_rushing_yard",
    "team_one_receiving_yard_player_image","team_one_receiving_yard_player_name","team_one_receiving_yard_player_position","team_one_receiving_yard_player_game_state","team_one_player_one_receiving_yard",
    "team_two_receiving_yard_player_image","team_two_receiving_yard_player_name","team_two_receiving_yard_player_position","team_two_receiving_yard_player_game_state","team_two_player_two_receiving_yard",
    "team_one_sacks_player_image","team_one_sacks_player_name","team_one_sacks_player_position","team_one_player_one_sacks","team_two_sacks_player_image","team_two_sacks_player_name","team_two_sacks_player_position","team_two_player_two_sacks",
    "team_one_tackles_player_image","team_one_tackles_player_name","team_one_tackles_player_position","team_one_tackles_player_game_state","team_one_player_one_tackles","team_two_tackles_player_image","team_two_tackles_player_name","team_two_tackles_player_position","team_two_tackles_player_game_state","team_two_player_two_tackles",
    "team_one_total_yards","team_two_total_yards","team_one_total_turnovers","team_two_total_turnovers","team_one_first_downs","team_two_first_downs","team_one_penalties","team_two_penalties","team_one_third_down","team_two_third_down","team_one_forth_down","team_two_forth_down","team_one_red_zone","team_two_red_zone","team_one_possession","team_two_possession"
]

# Open the CSV file and write the headers
live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
live_csv_writer = csv.writer(live_csv_file)
live_csv_writer.writerow(live_headers)

# --- LOAD PREVIOUSLY SCRAPED GAMES ---
finished_games = []
scraped_games_file = 'scraped_games.txt'

try:
    with open(scraped_games_file, 'r') as f:
        finished_games = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(finished_games)} previously scraped game(s).")
except FileNotFoundError:
    print("No previous scraped games file found. Starting fresh.")
    finished_games = []

# --- FUNCTION TO SAVE SCRAPED GAME ID ---
def save_scraped_game(game_id):
    """Save a FINAL game ID to the file to prevent re-scraping.
    Note: This should only be called for FINAL games, not LIVE games."""
    with open(scraped_games_file, 'a') as f:
        f.write(game_id + '\n')
    print(f"✓ Saved FINAL game ID '{game_id}' to prevent future re-scraping.")

# --- SIMPLE DATABASE PROCESSING ---
# All database functions are now in simple_db_helpers.py

try:
    game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
    num_days = len(game_sections)
    print("-----------------------------------------------")
    print(f"The number of days found is: {num_days}")
    print("-----------------------------------------------")
    print("\n")

    # --- FIRST PASS: Check if there are any FINAL games ---
    final_games_found = False
    
    for i in range(num_days):
        games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
        number_of_games_in_day = len(games_in_day)
        
        for j in range(number_of_games_in_day):
            try:
                game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
                game_status = driver.find_element(By.XPATH, game_status_xpath).text
            except NoSuchElementException:
                game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
                game_status = driver.find_element(By.XPATH, game_status_xpath).text
            
            if game_status == "FINAL":
                final_games_found = True
                break
        
        if final_games_found:
            break
    
    # Print what we found
    if final_games_found:
        print("========================================")
        print("FINAL games found! Scraping FINAL games only.")
        print("========================================")
        print("\n")
    else:
        print("========================================")
        print("No FINAL games found. Looking for LIVE games.")
        print("========================================")
        print("\n")

    # --- SECOND PASS: Scrape games based on what we found ---
    for i in range(num_days):
        games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
        number_of_games_in_day = len(games_in_day)
        game_date = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/header/div[1]/h3").text
        print("-----------------------------------------------")
        print(f"For {game_date}: The number of games is: {number_of_games_in_day}")
        print("-----------------------------------------------")
        print("\n")

        for j in range(number_of_games_in_day):
            try:
                game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
                game_status = driver.find_element(By.XPATH, game_status_xpath).text
            except NoSuchElementException:
                game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
                game_status = driver.find_element(By.XPATH, game_status_xpath).text

            # --- CODE TO ADD ---
            # Get the Gamecast URL and extract the unique game ID
            try:
                gamecast_link_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
                gamecast_url = gamecast_link_element.get_attribute('href')
                game_id = gamecast_url.split('/')[-1]
            except NoSuchElementException:
                # Handle cases where the gamecast link might not be available
                print("Gamecast link not found.")
                continue

            # The main check: if the game hasn't been scraped yet
            if game_id not in finished_games:
                if game_status == "FINAL":
                    try:
                        print("Scraping a FINAL game.")
                        click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
                        click_gamecast_button.click()
                        # Add the game ID to the list to prevent future scraping
                        finished_games.append(game_id)
                        save_scraped_game(game_id)
                    except NoSuchElementException:
                        print("Click Gamecast button not found.")
                        continue

                    time.sleep(5)

                    try:
                        team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/a/picture/img")
                        team_one_logo = team_one_logo_element.get_attribute('src') 
                        print(f"Team 1 logo: {team_one_logo}")
                    except NoSuchElementException:
                        try:
                            team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/a/picture/img")
                            team_one_logo = team_one_logo_element.get_attribute('src')
                            print(f"Team 1 logo: {team_one_logo}")
                        except NoSuchElementException:
                            team_one_logo = "N/A"
                            print(f"Team 1 logo: {team_one_logo}")
                            
                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/div/div/div[1]/div/a/span[1]").text
                        print(f"Team 1 Name: {team_one_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div/div/div[1]/div/a/span[2]").text
                            print(f"Team 1 Name: {team_one_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_name = "N/A"
                            print(f"Team 1 Name: {team_one_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[2]/div[1]").text
                        print(f"Team 1 Score: {team_one_score}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[2]/div[1]").text
                            print(f"Team 1 Score: {team_one_score}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_score = "N/A"
                            print(f"Team 1 Score: {team_one_score}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/div/div/div[2]/span[1]").text
                        print(f"Team 1 Record: {team_one_records}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div/div/div[2]/span").text
                            print(f"Team 1 Record: {team_one_records}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_records = "N/A"
                            print(f"Team 1 Record: {team_one_records}")

                    try:
                        team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/a/picture/img")
                        team_two_logo = team_two_logo_element.get_attribute('src') 
                        print(f"Team 1 logo: {team_two_logo}")
                    except NoSuchElementException:
                        try:
                            team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/a/picture/img")
                            team_two_logo = team_two_logo_element.get_attribute('src')
                            print(f"Team 1 logo: {team_two_logo}")
                        except NoSuchElementException:
                            team_two_logo = "N/A"
                            print(f"Team 1 logo: {team_two_logo}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
                        print(f"Team 2 Name: {team_two_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
                            print(f"Team 2 Name: {team_two_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_name = "N/A"
                            print(f"Team 2 Name: {team_two_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[2]/div[1]").text
                        print(f"Team 2 Score: {team_two_score}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[2]/div[1]").text
                            print(f"Team 2 Score: {team_two_score}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_score = "N/A"
                            print(f"Team 2 Score: {team_two_score}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/div/div/div[2]/span[1]").text
                        print(f"Team 2 Record: {team_two_records}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/div/div/div[2]/span").text
                            print(f"Team 2 Record: {team_two_records}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_records = "N/A"
                            print(f"Team 2 Record: {team_two_records}")

                    print("\n--------------------------------")
                    print("Game Leaders")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")
                        except NoSuchElementException:
                            team_one_passing_yard_player_image = "N/A"
                            print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_name = "N/A"
                            print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_position = "N/A"
                            print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_game_state = "N/A"
                            print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One Passing Yard: {team_one_player_one_passing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_passing_yard = "N/A"
                            print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
                        except NoSuchElementException:
                            team_two_passing_yard_player_image = "N/A"
                            print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_name = "N/A"
                            print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_position = "N/A"
                            print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_game_state = "N/A"
                            print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two Passing Yard: {team_two_player_two_passing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_passing_yard = "N/A"
                            print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")

                    
                    print("\n--------------------------------")
                    print("Rushing Yards")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")
                        except NoSuchElementException:
                            team_one_rushing_yard_player_image = "N/A"
                            print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_name = "N/A"
                            print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_position = "N/A"
                            print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_game_state = "N/A"
                            print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One rushing Yard: {team_one_player_one_rushing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_rushing_yard = "N/A"
                            print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
                        except NoSuchElementException:
                            team_two_rushing_yard_player_image = "N/A"
                            print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_name = "N/A"
                            print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_position = "N/A"
                            print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_game_state = "N/A"
                            print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two rushing Yard: {team_two_player_two_rushing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_rushing_yard = "N/A"
                            print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")

                    print("\n--------------------------------")
                    print("Receiving Yards")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
                        except NoSuchElementException:
                            team_one_receiving_yard_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_game_state = "N/A"
                            print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_receiving_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_receiving_yard = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
                        except NoSuchElementException:
                            team_two_receiving_yard_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_game_state = "N/A"
                            print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_receiving_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_receiving_yard = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")

                    print("\n--------------------------------")
                    print("Sacks")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_sacks_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_sacks_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
                        except NoSuchElementException:
                            team_one_sacks_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_sacks_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_sacks_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_sacks}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_sacks = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_sacks_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_sacks_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
                        except NoSuchElementException:
                            team_two_sacks_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_sacks_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_sacks_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_sacks}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_sacks = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")

                    print("\n--------------------------------")
                    print("Tackles")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_tackles_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_tackles_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")
                        except NoSuchElementException:
                            team_one_tackles_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_game_state = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_game_state = "N/A"
                            print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_tackles}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_tackles = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_tackles_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_tackles_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
                        except NoSuchElementException:
                            team_two_tackles_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_game_state = "N/A"
                            print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_tackles}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_tackles = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")

                    print("\n---------------------------------------------")
                    print("Team Stats")
                    print("------------------------------------------------\n")

                    print("\n-------------------------------------------------")
                    print("Total Yards")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[2]/div[1]/p[1]/span").text
                        print(f"Team 1 Total Yards: {team_one_total_yards}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total Yards: {team_one_total_yards}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_total_yards = "N/A"
                            print(f"Team 1 Total Yards: {team_one_total_yards}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[2]/div[1]/p[3]/span").text
                        print(f"Team 2 Total Yards: {team_two_total_yards}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total Yards: {team_two_total_yards}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_total_yards = "N/A"
                            print(f"Team 2 Total Yards: {team_two_total_yards}")

                    print("\n-------------------------------------------------")
                    print("Turnovers")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[3]/div[1]/p[1]/span").text
                        print(f"Team 1 Total turnovers: {team_one_total_turnovers}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total turnovers: {team_one_total_turnovers}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_total_turnovers = "N/A"
                            print(f"Team 1 Total turnovers: {team_one_total_turnovers}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[3]/div[1]/p[3]/span").text
                        print(f"Team 2 Total turnovers: {team_two_total_turnovers}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total turnovers: {team_two_total_turnovers}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_total_turnovers = "N/A"
                            print(f"Team 2 Total turnovers: {team_two_total_turnovers}")

                    print("\n-------------------------------------------------")
                    print("1st Downs")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[4]/div[1]/p[1]/span").text
                        print(f"Team 1 Total turnovers: {team_one_first_downs}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total turnovers: {team_one_first_downs}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_first_downs = "N/A"
                            print(f"Team 1 Total turnovers: {team_one_first_downs}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_first_downs = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[4]/div[1]/p[3]/span").text
                        print(f"Team 2 Total turnovers: {team_two_first_downs}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total turnovers: {team_two_first_downs}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_first_downs = "N/A"
                            print(f"Team 2 Total turnovers: {team_two_first_downs}")

                    print("\n-------------------------------------------------")
                    print("Penalties")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[5]/div[1]/p[1]/span").text
                        print(f"Team 1 Total penalties: {team_one_penalties}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total penalties: {team_one_penalties}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_penalties = "N/A"
                            print(f"Team 1 Total penalties: {team_one_penalties}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[5]/div[1]/p[3]/span").text
                        print(f"Team 2 Total penalties: {team_two_penalties}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total penalties: {team_two_penalties}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_penalties = "N/A"
                            print(f"Team 2 Total penalties: {team_two_penalties}")

                    print("\n-------------------------------------------------")
                    print("3rd Down")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[6]/div[1]/p[1]/span").text
                        print(f"Team 1 Total third_down: {team_one_third_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total third_down: {team_one_third_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_third_down = "N/A"
                            print(f"Team 1 Total third_down: {team_one_third_down}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[6]/div[1]/p[3]/span").text
                        print(f"Team 2 Total third_down: {team_two_third_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total third_down: {team_two_third_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_third_down = "N/A"
                            print(f"Team 2 Total third_down: {team_two_third_down}")

                    print("\n-------------------------------------------------")
                    print("4rd Down")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[7]/div[1]/p[1]/span").text
                        print(f"Team 1 Total forth_down: {team_one_forth_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total forth_down: {team_one_forth_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_forth_down = "N/A"
                            print(f"Team 1 Total forth_down: {team_one_forth_down}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[7]/div[1]/p[3]/span").text
                        print(f"Team 2 Total forth_down: {team_two_forth_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total forth_down: {team_two_forth_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_forth_down = "N/A"
                            print(f"Team 2 Total forth_down: {team_two_forth_down}")

                    print("\n-------------------------------------------------")
                    print("Red Zone")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[8]/div[1]/p[1]/span").text
                        print(f"Team 1 Total red_zone: {team_one_red_zone}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total red_zone: {team_one_red_zone}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_red_zone = "N/A"
                            print(f"Team 1 Total red_zone: {team_one_red_zone}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[8]/div[1]/p[3]/span").text
                        print(f"Team 2 Total red_zone: {team_two_red_zone}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total red_zone: {team_two_red_zone}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_red_zone = "N/A"
                            print(f"Team 2 Total red_zone: {team_two_red_zone}")

                    print("\n-------------------------------------------------")
                    print("Possession")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[9]/div[1]/p[1]/span").text
                        print(f"Team 1 Total possession: {team_one_possession}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total possession: {team_one_possession}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_possession = "N/A"
                            print(f"Team 1 Total possession: {team_one_possession}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[9]/div[1]/p[3]/span").text
                        print(f"Team 2 Total possession: {team_two_possession}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total possession: {team_two_possession}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_possession = "N/A"
                            print(f"Team 2 Total possession: {team_two_possession}")
                    
                    # --- DATABASE INSERTION FOR FINAL GAME ---
                    try:
                        # Create game data dictionary
                        game_data = create_game_data_dict(
                            team_one_logo, team_one_name, team_one_score, team_one_records,
                            team_two_logo, team_two_name, team_two_score, team_two_records,
                            team_one_passing_yard_player_image, team_one_passing_yard_player_name,
                            team_one_passing_yard_player_position, team_one_passing_yard_player_game_state,
                            team_one_player_one_passing_yard, team_two_passing_yard_player_image,
                            team_two_passing_yard_player_name, team_two_passing_yard_player_position,
                            team_two_passing_yard_player_game_state, team_two_player_two_passing_yard,
                            team_one_rushing_yard_player_image, team_one_rushing_yard_player_name,
                            team_one_rushing_yard_player_position, team_one_rushing_yard_player_game_state,
                            team_one_player_one_rushing_yard, team_two_rushing_yard_player_image,
                            team_two_rushing_yard_player_name, team_two_rushing_yard_player_position,
                            team_two_rushing_yard_player_game_state, team_two_player_two_rushing_yard,
                            team_one_receiving_yard_player_image, team_one_receiving_yard_player_name,
                            team_one_receiving_yard_player_position, team_one_receiving_yard_player_game_state,
                            team_one_player_one_receiving_yard, team_two_receiving_yard_player_image,
                            team_two_receiving_yard_player_name, team_two_receiving_yard_player_position,
                            team_two_receiving_yard_player_game_state, team_two_player_two_receiving_yard,
                            team_one_sacks_player_image, team_one_sacks_player_name, team_one_sacks_player_position,
                            team_one_player_one_sacks, team_two_sacks_player_image, team_two_sacks_player_name,
                            team_two_sacks_player_position, team_two_player_two_sacks,
                            team_one_tackles_player_image, team_one_tackles_player_name, team_one_tackles_player_position,
                            team_one_tackles_player_game_state, team_one_player_one_tackles, team_two_tackles_player_image,
                            team_two_tackles_player_name, team_two_tackles_player_position, team_two_tackles_player_game_state,
                            team_two_player_two_tackles, team_one_total_yards, team_two_total_yards,
                            team_one_total_turnovers, team_two_total_turnovers, team_one_first_downs,
                            team_two_first_downs, team_one_penalties, team_two_penalties, team_one_third_down,
                            team_two_third_down, team_one_forth_down, team_two_forth_down, team_one_red_zone,
                            team_two_red_zone, team_one_possession, team_two_possession
                        )
                        
                        # Move game to final_games table
                        if move_game_to_final(game_data):
                            print(f"✓ Successfully moved FINAL game to database: {team_one_name} vs {team_two_name}")
                        else:
                            print(f"❌ Failed to move FINAL game to database: {team_one_name} vs {team_two_name}")
                    
                    except Exception as e:
                        print(f"Error processing FINAL game: {e}")
                    
                    # Still write to CSV for backup
                    final_data = [team_one_logo,team_one_name,team_one_score,team_one_records,team_two_logo,team_two_name,team_two_score,team_two_records,
                                team_one_passing_yard_player_image,team_one_passing_yard_player_name,team_one_passing_yard_player_position,team_one_passing_yard_player_game_state,team_one_player_one_passing_yard,
                                team_two_passing_yard_player_image,team_two_passing_yard_player_name,team_two_passing_yard_player_position,team_two_passing_yard_player_game_state,team_two_player_two_passing_yard,
                                team_one_rushing_yard_player_image,team_one_rushing_yard_player_name,team_one_rushing_yard_player_position,team_one_rushing_yard_player_game_state,team_one_player_one_rushing_yard,
                                team_two_rushing_yard_player_image,team_two_rushing_yard_player_name,team_two_rushing_yard_player_position,team_two_rushing_yard_player_game_state,team_two_player_two_rushing_yard,
                                team_one_receiving_yard_player_image,team_one_receiving_yard_player_name,team_one_receiving_yard_player_position,team_one_receiving_yard_player_game_state,team_one_player_one_receiving_yard,
                                team_two_receiving_yard_player_image,team_two_receiving_yard_player_name,team_two_receiving_yard_player_position,team_two_receiving_yard_player_game_state,team_two_player_two_receiving_yard,
                                team_one_sacks_player_image,team_one_sacks_player_name,team_one_sacks_player_position,team_one_player_one_sacks,team_two_sacks_player_image,team_two_sacks_player_name,team_two_sacks_player_position,team_two_player_two_sacks,
                                team_one_tackles_player_image,team_one_tackles_player_name,team_one_tackles_player_position,team_one_tackles_player_game_state,team_one_player_one_tackles,team_two_tackles_player_image,team_two_tackles_player_name,team_two_tackles_player_position,team_two_tackles_player_game_state,team_two_player_two_tackles, 
                                team_one_total_yards,team_two_total_yards,team_one_total_turnovers,team_two_total_turnovers,team_one_first_downs,team_two_first_downs,team_one_penalties,team_two_penalties,team_one_third_down,team_two_third_down,team_one_forth_down,team_two_forth_down,team_one_red_zone,team_two_red_zone,team_one_possession,team_two_possession
                                ]
                    final_csv_writer.writerow(final_data)
                    
                    driver.back()

                elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
                    # --- SCRAPING AND PRINTING ALL LIVE DATA ---
                    print("----------------------------------------")
                    print(f"Game is still in progress: {game_status}")

                    try:
                        print("Scraping a LIVE game.")
                        click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[1]/div/section[{j+1}]/div[2]/a[1]")
                        click_gamecast_button.click()
                        # Note: We don't save LIVE games to prevent re-scraping since they can change during the game
                    except NoSuchElementException:
                        print("Click Gamecast button not found.")
                        continue

                    time.sleep(5)

                    try:
                        team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/a/picture/img")
                        team_one_logo = team_one_logo_element.get_attribute('src') 
                        print(f"Team 1 logo: {team_one_logo}")
                    except NoSuchElementException:
                        try:
                            team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/a/picture/img")
                            team_one_logo = team_one_logo_element.get_attribute('src')
                            print(f"Team 1 logo: {team_one_logo}")
                        except NoSuchElementException:
                            team_one_logo = "N/A"
                            print(f"Team 1 logo: {team_one_logo}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[1]/div/a/span[1]").text
                        print(f"Team 1 Name: {team_one_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[1]/div/a/span[2]").text
                            print(f"Team 1 Name: {team_one_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_name = "N/A"
                            print(f"Team 1 Name: {team_one_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[2]/div[1]").text
                        print(f"Team 1 Score: {team_one_score}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[2]/div[1]").text
                            print(f"Team 1 Score: {team_one_score}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_score = "N/A"
                            print(f"Team 1 Score: {team_one_score}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[2]/span[1]").text
                        print(f"Team 1 Record: {team_one_records}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[2]/span[1]").text
                            print(f"Team 1 Record: {team_one_records}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_records = "N/A"
                            print(f"Team 1 Record: {team_one_records}")

                    try:
                        team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/a/picture/img")
                        team_two_logo = team_two_logo_element.get_attribute('src') 
                        print(f"Team 1 logo: {team_two_logo}")
                    except NoSuchElementException:
                        try:
                            team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/a/picture/img")
                            team_two_logo = team_two_logo_element.get_attribute('src')
                            print(f"Team 1 logo: {team_two_logo}")
                        except NoSuchElementException:
                            team_two_logo = "N/A"
                            print(f"Team 1 logo: {team_two_logo}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
                        print(f"Team 2 Name: {team_two_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second one
                            team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
                            print(f"Team 2 Name: {team_two_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_name = "N/A"
                            print(f"Team 2 Name: {team_two_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[2]/div[1]").text
                        print(f"Team 2 Score: {team_two_score}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[2]/div[1]").text
                            print(f"Team 2 Score: {team_two_score}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_score = "N/A"
                            print(f"Team 2 Score: {team_two_score}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[2]/span[1]").text
                        print(f"Team 2 Record: {team_two_records}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[2]/span[1]").text
                            print(f"Team 2 Record: {team_two_records}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_records = "N/A"
                            print(f"Team 2 Record: {team_two_records}")

                    # try:
                    #     # First attempt: Try to find the element using the first XPath
                    #     yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div[2]/div[1]/span[2]").text
                    #     print(f"Yards: {yards}")
                    # except NoSuchElementException:
                    #     try:
                    #         # Second attempt: If the first XPath failed, try the second two
                    #         yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[1]/div[3]").text
                    #         print(f"Yards: {yards}")
                    #     except NoSuchElementException:
                    #         # Final fallback: If both XPaths failed, set the variable to "N/A"
                    #         yards = "N/A"
                    #         print(f"Yards: {yards}")

                    # try:
                    #     ball_on = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[1]/div[3]/p[2]").text
                    #     print(f"Ball On: {ball_on}")
                    # except NoSuchElementException:
                    #     try:
                    #         ball_on = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[1]/div[3]/p[1]").text
                    #         print(f"Ball On: {ball_on}")
                    #     except NoSuchElementException:
                    #         ball_on = "N/A"
                    #         print(f"Ball On: {ball_on}")

                    try:
                        place_to_watch = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[2]/button/p").text
                        print(f"Place to Watch: {place_to_watch}")
                    except NoSuchElementException:
                        try:
                            place_to_watch = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[2]/button/p").text
                            print(f"Place to Watch: {place_to_watch}")
                        except NoSuchElementException:
                            place_to_watch = "N/A";
                            print(f"Place to Watch: {place_to_watch}")

                    print("\n")
                    print("----------------------------------------")
                    print("Game Leaders")
                    print("----------------------------------------")
                    print("\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 1 Passing Yard Player Image: {team_one_passing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 1 Passing Yard Player Image: {team_one_passing_yard_player_image}")
                        except NoSuchElementException:
                            team_one_passing_yard_player_image = "N/A"
                            print(f"Team 1 Passing Yard Player Image: {team_one_passing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_name = "N/A"
                            print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_position = "N/A"
                            print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_passing_yard_player_game_state = "N/A"
                            print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One Passing Yard: {team_one_player_one_passing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_passing_yard = "N/A"
                            print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
                        except NoSuchElementException:
                            team_two_passing_yard_player_image = "N/A"
                            print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_name = "N/A"
                            print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_position = "N/A"
                            print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_passing_yard_player_game_state = "N/A"
                            print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two Passing Yard: {team_two_player_two_passing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_passing_yard = "N/A"
                            print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")

                    
                    print("\n--------------------------------")
                    print("Rushing Yards")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")
                        except NoSuchElementException:
                            team_one_rushing_yard_player_image = "N/A"
                            print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_name = "N/A"
                            print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_position = "N/A"
                            print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_rushing_yard_player_game_state = "N/A"
                            print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One rushing Yard: {team_one_player_one_rushing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_rushing_yard = "N/A"
                            print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
                        except NoSuchElementException:
                            team_two_rushing_yard_player_image = "N/A"
                            print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_name = "N/A"
                            print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_position = "N/A"
                            print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_rushing_yard_player_game_state = "N/A"
                            print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two rushing Yard: {team_two_player_two_rushing_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_rushing_yard = "N/A"
                            print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")

                    print("\n--------------------------------")
                    print("Receiving Yards")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
                        except NoSuchElementException:
                            team_one_receiving_yard_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_receiving_yard_player_game_state = "N/A"
                            print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_receiving_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_receiving_yard = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
                        except NoSuchElementException:
                            team_two_receiving_yard_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_receiving_yard_player_game_state = "N/A"
                            print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_receiving_yard}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_receiving_yard = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")

                    print("\n--------------------------------")
                    print("Sacks")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/a/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_sacks_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_sacks_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
                        except NoSuchElementException:
                            team_one_sacks_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/a/div/div[2]/div[1]/div/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_sacks_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/a/div/div[2]/div[1]/div/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_sacks_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/a/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_sacks}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_sacks = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/div/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_sacks_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_sacks_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
                        except NoSuchElementException:
                            team_two_sacks_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_sacks_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_sacks_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_sacks}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_sacks = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")

                    print("\n--------------------------------")
                    print("Tackles")
                    print("--------------------------------\n")

                    try:
                        team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
                        full_image_url = team_one_image_element.get_attribute('src') 
                        team_one_tackles_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")
                    except NoSuchElementException:
                        try:
                            team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
                            full_image_url = team_one_image_element.get_attribute('src')
                            team_one_tackles_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")
                        except NoSuchElementException:
                            team_one_tackles_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_name = "N/A"
                            print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_position = "N/A"
                            print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_tackles_player_game_state = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_tackles_player_game_state = "N/A"
                            print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Player One receiving Yard: {team_one_player_one_tackles}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
                            print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_player_one_tackles = "N/A"
                            print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")

                    try:
                        team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[4]/div/div/div[1]/picture/img")
                        full_image_url = team_two_image_element.get_attribute('src') 
                        team_two_tackles_player_image = full_image_url.split('&', 1)[0]
                        print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
                    except NoSuchElementException:
                        try:
                            team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[1]/picture/img")
                            full_image_url = team_two_image_element.get_attribute('src')
                            team_two_tackles_player_image = full_image_url.split('&', 1)[0]
                            print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
                        except NoSuchElementException:
                            team_two_tackles_player_image = "N/A"
                            print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                        print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
                            print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_name = "N/A"
                            print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                        print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
                            print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_position = "N/A"
                            print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
                        print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
                            print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_tackles_player_game_state = "N/A"
                            print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 2 Player two receiving Yard: {team_two_player_two_tackles}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_player_two_tackles = "N/A"
                            print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")

                    print("\n---------------------------------------------")
                    print("Team Stats")
                    print("------------------------------------------------\n")

                    print("\n-------------------------------------------------")
                    print("Total Yards")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                        print(f"Team 1 Total Yards: {team_one_total_yards}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total Yards: {team_one_total_yards}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_total_yards = "N/A"
                            print(f"Team 1 Total Yards: {team_one_total_yards}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[2]/div[1]/p[3]/span").text
                        print(f"Team 2 Total Yards: {team_two_total_yards}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_total_yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total Yards: {team_two_total_yards}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_total_yards = "N/A"
                            print(f"Team 2 Total Yards: {team_two_total_yards}")

                    print("\n-------------------------------------------------")
                    print("Turnovers")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[3]/div[1]/p[1]/span").text
                        print(f"Team 1 Total turnovers: {team_one_total_turnovers}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total turnovers: {team_one_total_turnovers}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_total_turnovers = "N/A"
                            print(f"Team 1 Total turnovers: {team_one_total_turnovers}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[3]/div[1]/p[3]/span").text
                        print(f"Team 2 Total turnovers: {team_two_total_turnovers}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_total_turnovers = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total turnovers: {team_two_total_turnovers}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_total_turnovers = "N/A"
                            print(f"Team 2 Total turnovers: {team_two_total_turnovers}")

                    print("\n-------------------------------------------------")
                    print("1st Downs")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[4]/div[1]/p[1]/span").text
                        print(f"Team 1 Total turnovers: {team_one_first_downs}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total turnovers: {team_one_first_downs}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_first_downs = "N/A"
                            print(f"Team 1 Total turnovers: {team_one_first_downs}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[4]/div[1]/p[3]/span").text
                        print(f"Team 2 Total turnovers: {team_two_first_downs}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_first_downs = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total turnovers: {team_two_first_downs}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_first_downs = "N/A"
                            print(f"Team 2 Total turnovers: {team_two_first_downs}")

                    print("\n-------------------------------------------------")
                    print("Penalties")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[5]/div[1]/p[1]/span").text
                        print(f"Team 1 Total penalties: {team_one_penalties}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total penalties: {team_one_penalties}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_penalties = "N/A"
                            print(f"Team 1 Total penalties: {team_one_penalties}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[5]/div[1]/p[3]/span").text
                        print(f"Team 2 Total penalties: {team_two_penalties}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_penalties = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total penalties: {team_two_penalties}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_penalties = "N/A"
                            print(f"Team 2 Total penalties: {team_two_penalties}")

                    print("\n-------------------------------------------------")
                    print("3rd Down")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[6]/div[1]/p[1]/span").text
                        print(f"Team 1 Total third_down: {team_one_third_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total third_down: {team_one_third_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_third_down = "N/A"
                            print(f"Team 1 Total third_down: {team_one_third_down}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[6]/div[1]/p[3]/span").text
                        print(f"Team 2 Total third_down: {team_two_third_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_third_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total third_down: {team_two_third_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_third_down = "N/A"
                            print(f"Team 2 Total third_down: {team_two_third_down}")

                    print("\n-------------------------------------------------")
                    print("4rd Down")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[7]/div[1]/p[1]/span").text
                        print(f"Team 1 Total forth_down: {team_one_forth_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total forth_down: {team_one_forth_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_forth_down = "N/A"
                            print(f"Team 1 Total forth_down: {team_one_forth_down}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[7]/div[1]/p[3]/span").text
                        print(f"Team 2 Total forth_down: {team_two_forth_down}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_forth_down = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total forth_down: {team_two_forth_down}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_forth_down = "N/A"
                            print(f"Team 2 Total forth_down: {team_two_forth_down}")

                    print("\n-------------------------------------------------")
                    print("Red Zone")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[8]/div[1]/p[1]/span").text
                        print(f"Team 1 Total red_zone: {team_one_red_zone}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total red_zone: {team_one_red_zone}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_red_zone = "N/A"
                            print(f"Team 1 Total red_zone: {team_one_red_zone}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[8]/div[1]/p[3]/span").text
                        print(f"Team 2 Total red_zone: {team_two_red_zone}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_red_zone = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total red_zone: {team_two_red_zone}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_red_zone = "N/A"
                            print(f"Team 2 Total red_zone: {team_two_red_zone}")

                    print("\n-------------------------------------------------")
                    print("Possession")
                    print("---------------------------------------------------\n")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_one_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[9]/div[1]/p[1]/span").text
                        print(f"Team 1 Total possession: {team_one_possession}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_one_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 1 Total possession: {team_one_possession}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_one_possession = "N/A"
                            print(f"Team 1 Total possession: {team_one_possession}")

                    try:
                        # First attempt: Try to find the element using the first XPath
                        team_two_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[3]/section/div[9]/div[1]/p[3]/span").text
                        print(f"Team 2 Total possession: {team_two_possession}")
                    except NoSuchElementException:
                        try:
                            # Second attempt: If the first XPath failed, try the second two
                            team_two_possession = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
                            print(f"Team 2 Total possession: {team_two_possession}")
                        except NoSuchElementException:
                            # Final fallback: If both XPaths failed, set the variable to "N/A"
                            team_two_possession = "N/A"
                            print(f"Team 2 Total possession: {team_two_possession}")
    
                    # --- DATABASE INSERTION FOR LIVE GAME ---
                    try:
                        # Create game data dictionary
                        game_data = create_game_data_dict(
                            team_one_logo, team_one_name, team_one_score, team_one_records,
                            team_two_logo, team_two_name, team_two_score, team_two_records,
                            team_one_passing_yard_player_image, team_one_passing_yard_player_name,
                            team_one_passing_yard_player_position, team_one_passing_yard_player_game_state,
                            team_one_player_one_passing_yard, team_two_passing_yard_player_image,
                            team_two_passing_yard_player_name, team_two_passing_yard_player_position,
                            team_two_passing_yard_player_game_state, team_two_player_two_passing_yard,
                            team_one_rushing_yard_player_image, team_one_rushing_yard_player_name,
                            team_one_rushing_yard_player_position, team_one_rushing_yard_player_game_state,
                            team_one_player_one_rushing_yard, team_two_rushing_yard_player_image,
                            team_two_rushing_yard_player_name, team_two_rushing_yard_player_position,
                            team_two_rushing_yard_player_game_state, team_two_player_two_rushing_yard,
                            team_one_receiving_yard_player_image, team_one_receiving_yard_player_name,
                            team_one_receiving_yard_player_position, team_one_receiving_yard_player_game_state,
                            team_one_player_one_receiving_yard, team_two_receiving_yard_player_image,
                            team_two_receiving_yard_player_name, team_two_receiving_yard_player_position,
                            team_two_receiving_yard_player_game_state, team_two_player_two_receiving_yard,
                            team_one_sacks_player_image, team_one_sacks_player_name, team_one_sacks_player_position,
                            team_one_player_one_sacks, team_two_sacks_player_image, team_two_sacks_player_name,
                            team_two_sacks_player_position, team_two_player_two_sacks,
                            team_one_tackles_player_image, team_one_tackles_player_name, team_one_tackles_player_position,
                            team_one_tackles_player_game_state, team_one_player_one_tackles, team_two_tackles_player_image,
                            team_two_tackles_player_name, team_two_tackles_player_position, team_two_tackles_player_game_state,
                            team_two_player_two_tackles, team_one_total_yards, team_two_total_yards,
                            team_one_total_turnovers, team_two_total_turnovers, team_one_first_downs,
                            team_two_first_downs, team_one_penalties, team_two_penalties, team_one_third_down,
                            team_two_third_down, team_one_forth_down, team_two_forth_down, team_one_red_zone,
                            team_two_red_zone, team_one_possession, team_two_possession
                        )
                        
                        # Insert/update live game
                        if insert_live_game(game_data):
                            print(f"✓ Successfully updated LIVE game in database: {team_one_name} vs {team_two_name}")
                        else:
                            print(f"❌ Failed to update LIVE game in database: {team_one_name} vs {team_two_name}")
                    
                    except Exception as e:
                        print(f"Error processing LIVE game: {e}")
                    
                    # Still write to CSV for backup
                    live_data = [team_one_logo,team_one_name,team_one_score,team_one_records,team_two_logo,team_two_name,team_two_score,team_two_records,
                                team_one_passing_yard_player_image,team_one_passing_yard_player_name,team_one_passing_yard_player_position,team_one_passing_yard_player_game_state,team_one_player_one_passing_yard,
                                team_two_passing_yard_player_image,team_two_passing_yard_player_name,team_two_passing_yard_player_position,team_two_passing_yard_player_game_state,team_two_player_two_passing_yard,
                                team_one_rushing_yard_player_image,team_one_rushing_yard_player_name,team_one_rushing_yard_player_position,team_one_rushing_yard_player_game_state,team_one_player_one_rushing_yard,
                                team_two_rushing_yard_player_image,team_two_rushing_yard_player_name,team_two_rushing_yard_player_position,team_two_rushing_yard_player_game_state,team_two_player_two_rushing_yard,
                                team_one_receiving_yard_player_image,team_one_receiving_yard_player_name,team_one_receiving_yard_player_position,team_one_receiving_yard_player_game_state,team_one_player_one_receiving_yard,
                                team_two_receiving_yard_player_image,team_two_receiving_yard_player_name,team_two_receiving_yard_player_position,team_two_receiving_yard_player_game_state,team_two_player_two_receiving_yard,
                                team_one_sacks_player_image,team_one_sacks_player_name,team_one_sacks_player_position,team_one_player_one_sacks,team_two_sacks_player_image,team_two_sacks_player_name,team_two_sacks_player_position,team_two_player_two_sacks,
                                team_one_tackles_player_image,team_one_tackles_player_name,team_one_tackles_player_position,team_one_tackles_player_game_state,team_one_player_one_tackles,team_two_tackles_player_image,team_two_tackles_player_name,team_two_tackles_player_position,team_two_tackles_player_game_state,team_two_player_two_tackles, 
                                team_one_total_yards,team_two_total_yards,team_one_total_turnovers,team_two_total_turnovers,team_one_first_downs,team_two_first_downs,team_one_penalties,team_two_penalties,team_one_third_down,team_two_third_down,team_one_forth_down,team_two_forth_down,team_one_red_zone,team_two_red_zone,team_one_possession,team_two_possession
                                ]
                    live_csv_writer.writerow(live_data)
                    driver.back()

                else:
                    print("--------------------------------------------------")
                    print(f"Game status is {game_status}. Skipping for now.")
                    print("--------------------------------------------------")
                    print("\n")
                    continue
            else:
                print("--------------------------------------------------")
                print(f"Game with ID '{game_id}' was already scraped previously.")
                print("Skipping to avoid duplicate scraping.")
                print("--------------------------------------------------")
                print("\n")
            
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    driver.quit()

finally:
    final_csv_file.close()
    live_csv_file.close()
    driver.quit()
