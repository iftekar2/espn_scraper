import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import os
import datetime


# --- SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# time.sleep(5)

# Get the current date and time
current_date = datetime.date.today()
print(f"Current date: {current_date}")

# A dictionary to map each week to its start date (Thursday)
week_start_dates = {
    1: datetime.date(2025, 9, 4),
    2: datetime.date(2025, 9, 11),
    3: datetime.date(2025, 9, 18),
    4: datetime.date(2025, 9, 25),
    5: datetime.date(2025, 10, 2),
    6: datetime.date(2025, 10, 9),
    7: datetime.date(2025, 10, 16),
    8: datetime.date(2025, 10, 23),
    9: datetime.date(2025, 10, 30),
    10: datetime.date(2025, 11, 6),
    11: datetime.date(2025, 11, 13),
    12: datetime.date(2025, 11, 20),
    13: datetime.date(2025, 11, 27),
    14: datetime.date(2025, 12, 4),
    15: datetime.date(2025, 12, 11),
    16: datetime.date(2025, 12, 18),
    17: datetime.date(2025, 12, 25),
    18: datetime.date(2026, 1, 1),
}

# This is to keep track of already scraped games
scraped_file = 'scraped_games.txt'
scraped_game_ids = set()

if os.path.exists(scraped_file):
    with open(scraped_file, 'r') as f:
        for line in f:
            scraped_game_ids.add(line.strip())

# This is to keep track of which week has be scraped
scraped_weeks_file = 'scraped_weeks.txt'
scraped_weeks = set()

if os.path.exists(scraped_weeks_file):
    with open(scraped_weeks_file, 'r') as f:
        for line in f:
            # Convert the line from a string to an integer
            scraped_weeks.add(int(line.strip()))

# --- CSV SETUP ---
final_headers = [
    "team_1_name", "team_1_score", "team_1_records", 
    "team_2_name", "team_2_score", "team_2_records", 
    "team_1_game_state", "team_2_game_state", 
    "team_1_logo", "team_2_logo",
    "pass_p1_name", "pass_p1_stats", "pass_p1_img", 
    "pass_p2_name", "pass_p2_stats", "pass_p2_img",
    "rush_p1_name", "rush_p1_stats", "rush_p1_img", 
    "rush_p2_name", "rush_p2_stats", "rush_p2_img",
    "rec_p1_name", "rec_p1_stats", "rec_p1_img", 
    "rec_p2_name", "rec_p2_stats", "rec_p2_img",
    "team_1_total_yards", "team_2_total_yards"
]

# Open the CSV file and write the headers
final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
final_csv_writer = csv.writer(final_csv_file)
final_csv_writer.writerow(final_headers)

live_headers = [
    "team_1_name", "team_1_records", "team_1_score", 
    "team_2_name", "team_2_records", "team_2_score", 
    "team_1_logo", "team_2_logo", "pass_p1_name", 
    "pass_p1_stats", "pass_p1_img", "pass_p2_name",
    "pass_p2_stats", "pass_p2_img", "rush_p1_name", 
    "rush_p1_stats", "rush_p1_img", "rush_p2_name", 
    "rush_p2_stats", "rush_p2_img", "rec_p1_name", 
    "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
    "rec_p2_stats", "rec_p2_img", "team_1_total_yards", 
    "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", 
    "team_1_first_downs","team_2_first_downs", "team_1_time_possession", 
    "team_2_time_possession"
]


# Open the CSV file and write the headers
live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
live_csv_writer = csv.writer(live_csv_file)
live_csv_writer.writerow(live_headers)

# The base URL for the NFL scoreboard
base_url = "https://www.espn.com/nfl/scoreboard/_/week/{week}/year/2025/seasontype/2"

# Iterate through all 18 regular season weeks
for week_number in range(1, 19):
    # Check if the current week has started
    if week_start_dates.get(week_number) is None or week_start_dates[week_number] > current_date:
        print(f"Week {week_number} has not yet started. Stopping the program.")
        break  # Exit the loop since all subsequent weeks are also in the future
    
    # Check if the week has already been scraped
    if week_number in scraped_weeks:
        print(f"Week {week_number} already scraped. Skipping.")
        continue  # Skip to the next week in the loop

    # If the week is in the past or present and hasn't been scraped,
    # proceed with scraping
    current_url = base_url.format(week=week_number)
    print(f"Navigating to: {current_url}")
    driver.get(current_url)


    try:
        game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
        num_games = len(game_sections)
        print(f"The number of games found is: {num_games}")

        for i in range(num_games):
            games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
            number_of_games_in_day = len(games_in_day)
            print(f"Day {i+1}: The number of games is: {number_of_games_in_day}")

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
                if game_id in scraped_game_ids:
                    print(f"Game with ID {game_id} already scraped. Skipping.")
                    continue
                else: 
                        if game_status == "FINAL":
                            try:
                                print("Scraping a FINAL game.")
                                click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
                                click_gamecast_button.click()
                            except NoSuchElementException:
                                print("Click Gamecast button not found.")
                                continue

                            time.sleep(5)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                print(f"Team 1 Name: {team_one_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[1]/div/section[2]/div[1]/div/div[1]/section/div/div/ul/li[1]/div[1]/div[1]/a/div").text
                                    print(f"Team 1 Name: {team_one_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_name = "N/A"
                                    print(f"Team 1 Name: {team_one_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                                print(f"Team 1 Score: {team_one_score}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                                    print(f"Team 1 Score: {team_one_score}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_score = "N/A"
                                    print(f"Team 1 Score: {team_one_score}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                                team_one_records = team_one_records.replace(" Away", "")
                                print(f"Team 1 Records: {team_one_records}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                                    team_one_records = team_one_records.replace(" Away", "")
                                    print(f"Team 1 Records: {team_one_records}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_records = "N/A"
                                    print(f"Team 1 Records: {team_one_records}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                print(f"Team 2 Name: {team_two_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second two
                                    team_two_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                    print(f"Team 2 Name: {team_two_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_name = "N/A"
                                    print(f"Team 2 Name: {team_two_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                                print(f"Team 2 Score: {team_two_score}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second two
                                    team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                                    print(f"Team 2 Score: {team_two_score}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_score = "N/A"
                                    print(f"Team 2 Score: {team_two_score}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                                team_two_records = team_two_records.replace(" Home", "")
                                print(f"Team 2 Records: {team_two_records}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                                    team_two_records = team_two_records.replace(" Home", "")
                                    print(f"Team 2 Records: {team_two_records}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_records = "N/A"
                                    print(f"Team 2 Records: {team_two_records}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                                print(f"Team One state: {team_one_game_state}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                                    print(f"Team One state: {team_one_game_state}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_game_state = "N/A"
                                    print(f"Team One state: {team_one_game_state}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                                print(f"Team Two Stat: {team_two_game_state}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                                    print(f"Team Two Stat: {team_two_game_state}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_game_state = "N/A"
                                    print(f"Team Two Stat: {team_two_game_state}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                                team_one_image = team_one_image_script.get_attribute('src')
                                print(f"Team 1 Logo: {team_one_image}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                                    team_one_image = team_one_image_script.get_attribute('src')
                                    print(f"Team 1 Logo: {team_one_image}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_image = "N/A"
                                    print(f"Team 1 Logo: {team_one_image}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                                team_two_image = team_two_image_script.get_attribute('src')
                                print(f"Team 2 Logo: {team_two_image}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                                    team_two_image = team_two_image_script.get_attribute('src')
                                    print(f"Team 2 Logo: {team_two_image}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_image = "N/A"
                                    print(f"Team 2 Logo: {team_two_image}")

                            #Passing Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_one_player_name = "N/A"
                                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                                print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_one_player_states = "N/A"
                                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                                click_passing_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                                    click_passing_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(2)

                            try:
                                passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                                print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Passing Yards Team 1 Player Image not found within the given time.")
                                passing_yard_team_one_player_image = "N/A"
                            
                            # Navigate back to the gamecast page
                            driver.back()

                            # Getting second Passing Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                                print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_two_player_name = "N/A"
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                                print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_two_player_states = "N/A"
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                                click_passing_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                                    click_passing_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(2)
                            try:
                                passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                                print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Passing Yards Team 2 Player Image not found within the given time.")
                                passing_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Rushing Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_one_player_name = "N/A"
                                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                                print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_one_player_states = "N/A"
                                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                                click_rushing_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                                    click_rushing_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass
                            
                            time.sleep(2)
                            try:
                                rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                                print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Rushing Yards Team 1 Player Image not found within the given time.")
                                rushing_yard_team_one_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Getting second rushing Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_two_player_name = "N/A"
                                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                                print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_two_player_states = "N/A"
                                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                                click_rushing_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                                    click_rushing_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(2)
                            try:
                                rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                                print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Rushing Yards Team 2 Player Image not found within the given time.")
                                rushing_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Receiving Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_one_player_name = "N/A"
                                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                                print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_one_player_states = "N/A"
                                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                                click_receiving_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                                    click_receiving_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(2)

                            try:
                                receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                                print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Receiving Yards Team 1 Player Image not found within the given time.")
                                receiving_yard_team_one_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Getting second receiving Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_two_player_name = "N/A"
                                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                                print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_two_player_states = "N/A"
                                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                                click_receiving_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                                    click_receiving_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(2)
                            try:
                                receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                                print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Receiving Yards Team 2 Player Image not found within the given time.")
                                receiving_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            time.sleep(3)
                            # Team Stats
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                                print(f"Team One Total Yards States : {team_one_total_yards_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
                                    print(f"Team One Total Yards States : {team_one_total_yards_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_total_yards_states = "N/A"
                                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                                print(f"Team Two Total Yards States : {team_two_total_yards_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_total_yards_states = "N/A"
                                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                            # Turnovers
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                                print(f"Team One Turnovers States : {team_one_turnovers_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                                    print(f"Team One Turnovers States : {team_one_turnovers_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_total_yards_states = "N/A"
                                    print(f"Team One Turnovers States : {team_one_turnovers_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                                print(f"Team Two Total Yards States : {team_two_turnovers_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_turnovers_states = "N/A"
                                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                            # 1st Downs
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                                print(f"Team One first_downs States : {team_one_first_downs_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                                    print(f"Team One first_downs States : {team_one_first_downs_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_first_downs_states = "N/A"
                                    print(f"Team One first_downs States : {team_one_first_downs_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
                                print(f"Team One Total 1st Downs States : {first_downs_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
                                    print(f"Team One Total 1st Downs States : {first_downs_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    first_downs_states = "N/A"
                                    print(f"Team One Total 1st Downs States : {first_downs_states}")
                            
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                                print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_first_downs_states = "N/A"
                                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                            
                            # Time of Possession
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[1]").text
                                print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[1]").text
                                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_time_of_possession_states = "N/A"
                                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                            
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[2]").text
                                print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[2]").text
                                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_time_of_possession_states = "N/A"
                                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

                            click_receiving_yard_team_two_player_name

                            final_data = [
                                team_one_name, team_one_score, team_one_records, 
                                team_two_name, team_two_score, team_two_records, 
                                team_one_game_state, team_two_game_state, 
                                team_one_image, team_two_image, 
                                passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
                                passing_yard_team_one_player_image, passing_yard_team_two_player_name, 
                                passing_yard_team_two_player_states, passing_yard_team_two_player_image, 
                                rushing_yard_team_one_player_name, rushing_yard_team_one_player_states, 
                                rushing_yard_team_one_player_image, rushing_yard_team_two_player_name, 
                                rushing_yard_team_two_player_states, rushing_yard_team_two_player_image, 
                                receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
                                receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
                                receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
                                team_one_total_yards_states, team_two_total_yards_states
                            ]
                            
                            final_csv_writer.writerow(final_data)

                            scraped_game_ids.add(game_id)
                            with open(scraped_file, 'a') as f:
                                f.write(game_id + '\n')
                            
                            driver.back()

                        elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
                            # --- SCRAPING AND PRINTING ALL LIVE DATA ---
                            print("----------------------------------------")
                            print(f"Game is still in progress: {game_status}")
                            
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                                click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                                    click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                print(f"Team One Name: {team_one_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                    print(f"Team One Name: {team_one_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_name = "N/A"
                                    print(f"Team One Name: {team_one_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                                print(f"Team 1 Records: {team_one_records}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                                    print(f"Team 1 Records: {team_one_records}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_records = "N/A"
                                    print(f"Team 1 Records: {team_one_records}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                                print(f"Team One Live Score: {team_one_live_score}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                                    print(f"Team One Live Score: {team_one_live_score}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_live_score = "N/A"
                                    print(f"Team One Live Score: {team_one_live_score}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                print(f"Team Two Name: {team_two_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                    print(f"Team Two Name: {team_two_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_name = "N/A"
                                    print(f"Team Two Name: {team_two_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                                team_two_records = team_two_records.replace(" Home", "")
                                print(f"Team 2 Records: {team_two_records}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                                    team_two_records = team_two_records.replace(" Home", "")
                                    print(f"Team 2 Records: {team_two_records}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_records = "N/A"
                                    print(f"Team 2 Records: {team_two_records}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                                print(f"Team Two Live Score: {team_two_live_score}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                                    print(f"Team Two Live Score: {team_two_live_score}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_live_score = "N/A"
                                    print(f"Team Two Live Score: {team_two_live_score}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                                team_one_image = team_one_image_script.get_attribute('src')
                                print(f"Team 1 Logo: {team_one_image}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                                    team_one_image = team_one_image_script.get_attribute('src')
                                    print(f"Team 1 Logo: {team_one_image}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_image = "N/A"
                                    print(f"Team 1 Logo: {team_one_image}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                                team_two_image = team_two_image_script.get_attribute('src')
                                print(f"Team 2 Logo: {team_two_image}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                                    team_two_image = team_two_image_script.get_attribute('src')
                                    print(f"Team 2 Logo: {team_two_image}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_image = "N/A"
                                    print(f"Team 2 Logo: {team_two_image}")

                            #Passing Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_one_player_name = "N/A"
                                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                                print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_one_player_name = "N/A"
                                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                            time.sleep(5)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                                click_passing_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                                    click_passing_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)
                            try:
                                passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                                print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Passing Yards Team 1 Player Image not found within the given time.")
                                passing_yard_team_one_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Getting second Passing Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                                print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_two_player_name = "N/A"
                                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                                print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                                    print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    passing_yard_team_two_player_states = "N/A"
                                    print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                                click_passing_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                                    click_passing_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)
                            try:
                                passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                                print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Passing Yards Team 2 Player Image not found within the given time.")
                                passing_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Rushing Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_one_player_name = "N/A"
                                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                                print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_one_player_states = "N/A"
                                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                                click_rushing_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                                    click_rushing_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)
                            try:
                                rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                                print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Rushing Yards Team 1 Player Image not found within the given time.")
                                rushing_yard_team_one_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Getting second rushing Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_two_player_name = "N/A"
                                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                                print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    rushing_yard_team_two_player_states = "N/A"
                                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                                click_rushing_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                                    click_rushing_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)

                            try:
                                rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                                print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Rushing Yards Team 2 Player Image not found within the given time.")
                                rushing_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Receiving Yards
                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_one_player_name = "N/A"
                                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                                print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_one_player_name = "N/A"
                                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                                click_receiving_yard_team_one_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                                    click_receiving_yard_team_one_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)

                            try:
                                receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                                print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
                            except TimeoutException:
                                print("Receiving Yards Team 1 Player Image not found within the given time.")
                                receiving_yard_team_one_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Getting second receiving Yards player data
                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_two_player_name = "N/A"
                                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                                print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    receiving_yard_team_two_player_states = "N/A"
                                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                            time.sleep(2)
                            try:
                                # First attempt: Try to find the element using the first XPath
                                click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                                click_receiving_yard_team_two_player_name.click()
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                                    click_receiving_yard_team_two_player_name.click()
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    pass

                            time.sleep(5)
                            try:
                                receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
                                    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
                                )
                                receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                                print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
                            except TimeoutException:
                                print("Receiving Yards Team 2 Player Image not found within the given time.")
                                receiving_yard_team_two_player_image = "N/A"

                            # Go back to the Match page
                            driver.back()

                            # Team Stats
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
                                print(f"Team One Total Yards States : {team_one_total_yards_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                                    print(f"Team One Total Yards States : {team_one_total_yards_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_total_yards_states = "N/A"
                                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                                print(f"Team Two Total Yards States : {team_two_total_yards_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_total_yards_states = "N/A"
                                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                            # Turnovers
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                                print(f"Team One Turnovers States : {team_one_turnovers_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                                    print(f"Team One Turnovers States : {team_one_turnovers_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_turnovers_states = "N/A"
                                    print(f"Team One Turnovers States : {team_one_turnovers_states}")
                            
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                                print(f"Team Two Total Yards States : {team_two_turnovers_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_turnovers_states = "N/A"
                                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                            # 1st Downs
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                                print(f"Team One first_downs States : {team_one_first_downs_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                                    print(f"Team One first_downs States : {team_one_first_downs_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_first_downs_states = "N/A"
                                    print(f"Team One first_downs States : {team_one_first_downs_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                                print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_first_downs_states = "N/A"
                                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                            
                            # Time of Possession
                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                                print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_one_time_of_possession_states = "N/A"
                                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

                            try:
                                # First attempt: Try to find the element using the first XPath
                                team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                                print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                            except NoSuchElementException:
                                try:
                                    # Second attempt: If the first XPath failed, try the second one
                                    team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
                                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                                except NoSuchElementException:
                                    # Final fallback: If both XPaths failed, set the variable to "N/A"
                                    team_two_time_of_possession_states = "N/A"
                                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                            
            
                            live_data = [team_one_name, team_one_records, team_one_live_score, team_two_name, team_two_records, team_two_live_score, team_one_image, 
                                        team_two_image, passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
                                        passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
                                        passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
                                        rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
                                        rushing_yard_team_two_player_name, rushing_yard_team_two_player_states, 
                                        rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states,
                                    receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
                                        receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
                                        team_one_total_yards_states, team_two_total_yards_states, team_one_turnovers_states, team_two_turnovers_states, 
                                        team_one_first_downs_states, team_two_first_downs_states, team_one_time_of_possession_states, team_two_time_of_possession_states]

                            live_csv_writer.writerow(live_data)
                            driver.back()

                        else:
                            print(f"Game status is {game_status}. Skipping for now.")
                            continue

                scraped_weeks.add(week_number)
            with open(scraped_weeks_file, 'a') as f:
                f.write(str(week_number) + '\n')
                
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        driver.quit()

    finally:
        final_csv_file.close()
        live_csv_file.close()
        driver.quit()


