import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
time.sleep(5)

# --- CSV SETUP ---
headers = [
    'Team One Name', 'Team One Score', 'Team One Location', 'Team One Logo',
    'Team Two Name', 'Team Two Score', 'Team Two Logo', 'Game Status',
    'Team One Scores by Quarter', 'Team Two Scores by Quarter',
    'Passing Yard Stat Name', 'Passing Yard Player One Image', 'Passing Yard Player One Team', 'Passing Yard Player One Name', 'Passing Yard Player One Stats',
    'Passing Yard Player Two Image', 'Passing Yard Player Two Team', 'Passing Yard Player Two Name', 'Passing Yard Player Two Stats',
    'Rushing Yard Stat Name', 'Rushing Yard Player One Image', 'Rushing Yard Player One Team', 'Rushing Yard Player One Name', 'Rushing Yard Player One Stats',
    'Rushing Yard Player Two Image', 'Rushing Yard Player Two Team', 'Rushing Yard Player Two Name', 'Rushing Yard Player Two Stats',
    'Receiving Yard Stat Name', 'Receiving Yard Player One Image', 'Receiving Yard Player One Team', 'Receiving Yard Player One Name', 'Receiving Yard Player One Stats',
    'Receiving Yard Player Two Image', 'Receiving Yard Player Two Team', 'Receiving Yard Player Two Name', 'Receiving Yard Player Two Stats',
    'Total Yards Team One', 'Total Yards Team Two',
    'Turnovers Team One', 'Turnovers Team Two',
    'First Downs Team One', 'First Downs Team Two'
]

csv_file = open('nfl_games.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(headers)


finished_games = []

# --- MAIN LOOP FOR SCRAPING EACH GAME ---
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

            if game_id not in finished_games: 
                # Add the game ID to the list to prevent future scraping
                finished_games.append(game_id)
                
                if game_status == "FINAL":
                    try:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                    except NoSuchElementException:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

                    time.sleep(5)

                    team_one_name_xpath = "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2"
        
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, team_one_name_xpath))
                    )
                    
                    team_one_name = driver.find_element(By.XPATH, team_one_name_xpath).text
                    print(f"Team 1 Name: {team_one_name}")
                    

                    try:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    print(f"Stat: {team_one_score}")

                    try:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    except NoSuchElementException:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    print(f"Team 1 Records: {team_one_records}")

                    try:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    except NoSuchElementException:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    print(f"Team 2 Records: {team_two_records}")

                    try:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    except NoSuchElementException:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    print(f"Stat: {team_one_live_score}")

                    try:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    except NoSuchElementException:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    print(f"Stat: {team_one_live_score}")

                    try:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    print(f"Team 1 Logo: {team_one_image}")

                    try:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    print(f"Team 2 Logo: {team_two_image}")

                    #Passing Yards
                    try:
                        passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
                    except NoSuchElementException:
                        passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
                    print(f"Passing Yards : {passing_yard_text}")

                    try:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                    try:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                    time.sleep(2)
                    try:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                    except NoSuchElementException:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                    click_passing_yard_team_one_player_name.click()

                    time.sleep(2)

                    try:
                        passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                    print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

                    # Go back to the Match page
                    driver.back()

                    # Getting second Passing Yards player data
                    try:
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                    try:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                    print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                    except NoSuchElementException:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                    click_passing_yard_team_two_player_name.click()

                    time.sleep(2)

                    try:
                        passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                    print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

                    # Go back to the Match page
                    driver.back()

                    # Rushing Yards
                    try:
                        rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
                    except NoSuchElementException:
                        rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
                    print(f"rushing Yards : {rushing_yard_text}")

                    try:
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                    try:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")


                    time.sleep(2)
                    try:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                    except NoSuchElementException:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                    click_rushing_yard_team_one_player_name.click()

                    time.sleep(2)

                    try:
                        rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                    print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

                    # Go back to the Match page
                    driver.back()

                    # Getting second rushing Yards player data
                    try:
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                    try:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                    except NoSuchElementException:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                    click_rushing_yard_team_two_player_name.click()

                    time.sleep(2)

                    try:
                        rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                    print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

                    # Go back to the Match page
                    driver.back()

                    # Receiving Yards
                    try:
                        receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
                    except NoSuchElementException:
                        receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
                    print(f"Receiving Yards : {receiving_yard_text}")

                    try:
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                    try:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                    time.sleep(2)
                    try:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                    except NoSuchElementException:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                    click_receiving_yard_team_one_player_name.click()

                    time.sleep(2)

                    try:
                        receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                    print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

                    # Go back to the Match page
                    driver.back()

                    # Getting second receiving Yards player data
                    try:
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                    try:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                    except NoSuchElementException:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                    click_receiving_yard_team_two_player_name.click()

                    time.sleep(2)

                    try:
                        receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                    except NoSuchElementException:
                        receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                        receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                    print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

                    # Go back to the Match page
                    driver.back()

                    time.sleep(3)
                    # Team Stats
                    try:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                    try:
                        total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
                    except NoSuchElementException:
                        total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
                    print(f"Team Two Total Yards States : {total_yards_states}")

                    try:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                    # Turnovers
                    try:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                    print(f"Team One Turnovers States : {team_one_turnovers_states}")

                    try:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
                    except NoSuchElementException:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
                    print(f"Team One Total Yards States : {turnovers_states}")
                    
                    try:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                    # 1st Downs
                    try:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                    print(f"Team One first_downs States : {team_one_first_downs_states}")

                    try:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
                    except NoSuchElementException:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
                    print(f"Team One Total 1st Downs States : {first_downs_states}")
                    
                    try:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
                    # Time of Possession
                    try:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                    except NoSuchElementException:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

                    try:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
                    except NoSuchElementException:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
                    print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                    
                    try:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                    except NoSuchElementException:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                    
                    driver.back()

            elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
                # --- SCRAPING AND PRINTING ALL LIVE DATA ---
                print("----------------------------------------")
                print(f"Game is still in progress: {game_status}")

                try:
                    click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                    click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                except NoSuchElementException:
                    click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                    click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

                try:
                    team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                                                   
                except NoSuchElementException:
                    team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                print(f"Stat: {team_one_name}")

                try:
                    team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                except NoSuchElementException:
                    team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                print(f"Stat: {team_one_score}")

                try:
                    team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                    team_one_records = team_one_records.replace(" Away", "")
                except NoSuchElementException:
                    team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                    team_one_records = team_one_records.replace(" Away", "")
                print(f"Team 1 Records: {team_one_records}")

                try:
                    team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                    team_two_records = team_two_records.replace(" Home", "")
                except NoSuchElementException:
                    team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                    team_two_records = team_two_records.replace(" Home", "")
                print(f"Team 2 Records: {team_two_records}")

                try:
                    team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                except NoSuchElementException:
                    team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                print(f"Stat: {team_one_live_score}")

                try:
                    team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                except NoSuchElementException:
                    team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                print(f"Stat: {team_one_live_score}")

                try:
                    team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                    team_one_image = team_one_image_script.get_attribute('src')
                except NoSuchElementException:
                    team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                    team_one_image = team_one_image_script.get_attribute('src')
                print(f"Team 1 Logo: {team_one_image}")

                try:
                    team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                    team_two_image = team_two_image_script.get_attribute('src')
                except NoSuchElementException:
                    team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                    team_two_image = team_two_image_script.get_attribute('src')
                print(f"Team 2 Logo: {team_two_image}")

                #Passing Yards
                try:
                    passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
                except NoSuchElementException:
                    passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
                print(f"Passing Yards : {passing_yard_text}")

                try:
                    passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                try:
                    passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                except NoSuchElementException:
                    passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                try:
                    click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                except NoSuchElementException:
                    click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[1]/section/div/div[2]/div[1]/section/div/a[1]")
                click_passing_yard_team_one_player_name.click()

                time.sleep(5)

                try:
                    passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
                print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

                # Go back to the Match page
                driver.back()

                # Getting second Passing Yards player data
                try:
                    passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                try:
                    passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                except NoSuchElementException:
                    passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

                try:
                    click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                except NoSuchElementException:
                    click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                click_passing_yard_team_two_player_name.click()

                time.sleep(5)

                try:
                    passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
                print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

                # Go back to the Match page
                driver.back()

                # Rushing Yards
                try:
                    rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
                except NoSuchElementException:
                    rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
                print(f"rushing Yards : {rushing_yard_text}")

                try:
                    rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                try:
                    rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                except NoSuchElementException:
                    rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

                try:
                    click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                except NoSuchElementException:
                    click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                click_rushing_yard_team_one_player_name.click()

                time.sleep(5)

                try:
                    rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
                print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

                # Go back to the Match page
                driver.back()

                # Getting second rushing Yards player data
                try:
                    rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                try:
                    rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                except NoSuchElementException:
                    rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                try:
                    click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                except NoSuchElementException:
                    click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                click_rushing_yard_team_two_player_name.click()

                time.sleep(5)

                try:
                    rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
                print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

                # Go back to the Match page
                driver.back()

                # Receiving Yards
                try:
                    receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
                except NoSuchElementException:
                    receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
                print(f"Receiving Yards : {receiving_yard_text}")

                try:
                    receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                try:
                    receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                except NoSuchElementException:
                    receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                try:
                    click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                except NoSuchElementException:
                    click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                click_receiving_yard_team_one_player_name.click()

                time.sleep(5)

                try:
                    receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
                print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

                # Go back to the Match page
                driver.back()

                # Getting second receiving Yards player data
                try:
                    receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                except NoSuchElementException:
                    receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                try:
                    receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                except NoSuchElementException:
                    receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                try:
                    click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                except NoSuchElementException:
                    click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                click_receiving_yard_team_two_player_name.click()

                time.sleep(5)

                try:
                    receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                except NoSuchElementException:
                    receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
                    receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
                print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

                # Go back to the Match page
                driver.back()

                # Team Stats
                try:
                    team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
                except NoSuchElementException:
                    team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                print(f"Team One Total Yards States : {team_one_total_yards_states}")

                try:
                    total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
                except NoSuchElementException:
                    total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
                print(f"Team Two Total Yards States : {total_yards_states}")

                try:
                    team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                except NoSuchElementException:
                    team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                # Turnovers
                try:
                    team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                except NoSuchElementException:
                    team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                print(f"Team One Turnovers States : {team_one_turnovers_states}")

                try:
                    turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
                except NoSuchElementException:
                    turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
                print(f"Team One Total Yards States : {turnovers_states}")
                
                try:
                    team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                except NoSuchElementException:
                    team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                # 1st Downs
                try:
                    team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                except NoSuchElementException:
                    team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                print(f"Team One first_downs States : {team_one_first_downs_states}")

                try:
                    first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
                except NoSuchElementException:
                    first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
                print(f"Team One Total 1st Downs States : {first_downs_states}")
                
                try:
                    team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                except NoSuchElementException:
                    team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                
                # Time of Possession
                try:
                    team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                except NoSuchElementException:
                    team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

                try:
                    time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
                except NoSuchElementException:
                    time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
                print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                
                try:
                    team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                except NoSuchElementException:
                    team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
                print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

                driver.back()

            else: 
                continue
            
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    driver.quit()

finally:
    csv_file.close()
    driver.quit()













# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.common.exceptions import NoSuchElementException
# import csv
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # --- SETUP ---
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# time.sleep(5)

# # --- CSV SETUP ---
# headers = [
#     'Team One Name', 'Team One Score', 'Team One Location', 'Team One Logo',
#     'Team Two Name', 'Team Two Score', 'Team Two Logo', 'Game Status',
#     'Team One Scores by Quarter', 'Team Two Scores by Quarter',
#     'Passing Yard Stat Name', 'Passing Yard Player One Image', 'Passing Yard Player One Team', 'Passing Yard Player One Name', 'Passing Yard Player One Stats',
#     'Passing Yard Player Two Image', 'Passing Yard Player Two Team', 'Passing Yard Player Two Name', 'Passing Yard Player Two Stats',
#     'Rushing Yard Stat Name', 'Rushing Yard Player One Image', 'Rushing Yard Player One Team', 'Rushing Yard Player One Name', 'Rushing Yard Player One Stats',
#     'Rushing Yard Player Two Image', 'Rushing Yard Player Two Team', 'Rushing Yard Player Two Name', 'Rushing Yard Player Two Stats',
#     'Receiving Yard Stat Name', 'Receiving Yard Player One Image', 'Receiving Yard Player One Team', 'Receiving Yard Player One Name', 'Receiving Yard Player One Stats',
#     'Receiving Yard Player Two Image', 'Receiving Yard Player Two Team', 'Receiving Yard Player Two Name', 'Receiving Yard Player Two Stats',
#     'Total Yards Team One', 'Total Yards Team Two',
#     'Turnovers Team One', 'Turnovers Team Two',
#     'First Downs Team One', 'First Downs Team Two'
# ]

# csv_file = open('nfl_games.csv', 'w', newline='', encoding='utf-8')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(headers)


# finished_games = []

# # --- MAIN LOOP FOR SCRAPING EACH GAME ---
# try:
#     game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
#     num_games = len(game_sections)
#     print(f"The number of games found is: {num_games}")

#     for i in range(num_games):
#         games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
#         number_of_games_in_day = len(games_in_day)
#         print(f"Day {i+1}: The number of games is: {number_of_games_in_day}")

#         for j in range(number_of_games_in_day): 
#             try:
#                 game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
#                 game_status = driver.find_element(By.XPATH, game_status_xpath).text
#             except NoSuchElementException:
#                 game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
#                 game_status = driver.find_element(By.XPATH, game_status_xpath).text
            
#             # --- CODE TO ADD ---
#             # Get the Gamecast URL and extract the unique game ID
#             try:
#                 gamecast_link_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
#                 gamecast_url = gamecast_link_element.get_attribute('href')
#                 game_id = gamecast_url.split('/')[-1]
#             except NoSuchElementException:
#                 # Handle cases where the gamecast link might not be available
#                 print("Gamecast link not found.")
#                 continue

#             if game_id not in finished_games: 
#                 # Add the game ID to the list to prevent future scraping
#                 finished_games.append(game_id)
                
#                 if game_status == "FINAL":
#                     try:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
#                     except NoSuchElementException:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

#                     time.sleep(5)

#                     team_one_name_xpath = "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2"
        
#                     WebDriverWait(driver, 10).until(
#                         EC.visibility_of_element_located((By.XPATH, team_one_name_xpath))
#                     )
                    
#                     team_one_name = driver.find_element(By.XPATH, team_one_name_xpath).text
#                     print(f"Team 1 Name: {team_one_name}")
                    

#                     try:
#                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     except NoSuchElementException:
#                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     print(f"Stat: {team_one_score}")

#                     try:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     except NoSuchElementException:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     print(f"Team 1 Records: {team_one_records}")

#                     try:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     except NoSuchElementException:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     print(f"Team 2 Records: {team_two_records}")

#                     try:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     except NoSuchElementException:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     print(f"Stat: {team_one_live_score}")

#                     try:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     except NoSuchElementException:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     print(f"Stat: {team_one_live_score}")

#                     try:
#                         team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
#                         team_one_image = team_one_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
#                         team_one_image = team_one_image_script.get_attribute('src')
#                     print(f"Team 1 Logo: {team_one_image}")

#                     try:
#                         team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
#                         team_two_image = team_two_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
#                         team_two_image = team_two_image_script.get_attribute('src')
#                     print(f"Team 2 Logo: {team_two_image}")

#                     #Passing Yards
#                     try:
#                         passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
#                     except NoSuchElementException:
#                         passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
#                     print(f"Passing Yards : {passing_yard_text}")

#                     try:
#                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

#                     try:
#                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                     except NoSuchElementException:
#                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                     print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
#                     click_passing_yard_team_one_player_name.click()

#                     time.sleep(2)

#                     try:
#                         passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                     print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second Passing Yards player data
#                     try:
#                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                     print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

#                     try:
#                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
#                     except NoSuchElementException:
#                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
#                     print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
#                     click_passing_yard_team_two_player_name.click()

#                     time.sleep(2)

#                     try:
#                         passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                     print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     # Rushing Yards
#                     try:
#                         rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
#                     except NoSuchElementException:
#                         rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
#                     print(f"rushing Yards : {rushing_yard_text}")

#                     try:
#                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

#                     try:
#                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                     except NoSuchElementException:
#                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                     print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")


#                     time.sleep(2)
#                     try:
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
#                     click_rushing_yard_team_one_player_name.click()

#                     time.sleep(2)

#                     try:
#                         rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                     print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second rushing Yards player data
#                     try:
#                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                     print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

#                     try:
#                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                     except NoSuchElementException:
#                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                     print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
#                     click_rushing_yard_team_two_player_name.click()

#                     time.sleep(2)

#                     try:
#                         rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                     print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     # Receiving Yards
#                     try:
#                         receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
#                     except NoSuchElementException:
#                         receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
#                     print(f"Receiving Yards : {receiving_yard_text}")

#                     try:
#                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

#                     try:
#                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                     except NoSuchElementException:
#                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                     print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
#                     click_receiving_yard_team_one_player_name.click()

#                     time.sleep(2)

#                     try:
#                         receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                     print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second receiving Yards player data
#                     try:
#                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                     print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

#                     try:
#                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                     except NoSuchElementException:
#                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                     print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
#                     click_receiving_yard_team_two_player_name.click()

#                     time.sleep(2)

#                     try:
#                         receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                     except NoSuchElementException:
#                         receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                     print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

#                     # Go back to the Match page
#                     driver.back()

#                     time.sleep(3)
#                     # Team Stats
#                     try:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
#                     except NoSuchElementException:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
#                     print(f"Team One Total Yards States : {team_one_total_yards_states}")

#                     try:
#                         total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
#                     except NoSuchElementException:
#                         total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
#                     print(f"Team Two Total Yards States : {total_yards_states}")

#                     try:
#                         team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
#                     except NoSuchElementException:
#                         team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
#                     print(f"Team Two Total Yards States : {team_two_total_yards_states}")

#                     # Turnovers
#                     try:
#                         team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
#                     except NoSuchElementException:
#                         team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
#                     print(f"Team One Turnovers States : {team_one_turnovers_states}")

#                     try:
#                         turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
#                     except NoSuchElementException:
#                         turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
#                     print(f"Team One Total Yards States : {turnovers_states}")
                    
#                     try:
#                         team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
#                     except NoSuchElementException:
#                         team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
#                     print(f"Team Two Total Yards States : {team_two_turnovers_states}")

#                     # 1st Downs
#                     try:
#                         team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
#                     except NoSuchElementException:
#                         team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
#                     print(f"Team One first_downs States : {team_one_first_downs_states}")

#                     try:
#                         first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
#                     except NoSuchElementException:
#                         first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
#                     print(f"Team One Total 1st Downs States : {first_downs_states}")
                    
#                     try:
#                         team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
#                     except NoSuchElementException:
#                         team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
#                     print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
#                     # Time of Possession
#                     try:
#                         team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
#                     except NoSuchElementException:
#                         team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
#                     print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

#                     try:
#                         time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
#                     except NoSuchElementException:
#                         time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
#                     print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                    
#                     try:
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
#                     except NoSuchElementException:
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
#                     print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                    
#                     driver.back()

#             elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
#                 # --- SCRAPING AND PRINTING ALL LIVE DATA ---
#                 print("----------------------------------------")
#                 print(f"Game is still in progress: {game_status}")

#                 try:
#                     click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                     click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
#                 except NoSuchElementException:
#                     click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                     click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

#                 try:
#                     team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                                                   
#                 except NoSuchElementException:
#                     team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                 print(f"Stat: {team_one_name}")

#                 try:
#                     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                 except NoSuchElementException:
#                     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                 print(f"Stat: {team_one_score}")

#                 try:
#                     team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
#                     team_one_records = team_one_records.replace(" Away", "")
#                 except NoSuchElementException:
#                     team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
#                     team_one_records = team_one_records.replace(" Away", "")
#                 print(f"Team 1 Records: {team_one_records}")

#                 try:
#                     team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
#                     team_two_records = team_two_records.replace(" Home", "")
#                 except NoSuchElementException:
#                     team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
#                     team_two_records = team_two_records.replace(" Home", "")
#                 print(f"Team 2 Records: {team_two_records}")

#                 try:
#                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                 except NoSuchElementException:
#                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                 print(f"Stat: {team_one_live_score}")

#                 try:
#                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                 except NoSuchElementException:
#                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                 print(f"Stat: {team_one_live_score}")

#                 try:
#                     team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
#                     team_one_image = team_one_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
#                     team_one_image = team_one_image_script.get_attribute('src')
#                 print(f"Team 1 Logo: {team_one_image}")

#                 try:
#                     team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
#                     team_two_image = team_two_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
#                     team_two_image = team_two_image_script.get_attribute('src')
#                 print(f"Team 2 Logo: {team_two_image}")

#                 #Passing Yards
#                 try:
#                     passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
#                 except NoSuchElementException:
#                     passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
#                 print(f"Passing Yards : {passing_yard_text}")

#                 try:
#                     passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

#                 try:
#                     passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                 except NoSuchElementException:
#                     passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

#                 try:
#                     click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
#                 except NoSuchElementException:
#                     click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[1]/section/div/div[2]/div[1]/section/div/a[1]")
#                 click_passing_yard_team_one_player_name.click()

#                 time.sleep(5)

#                 try:
#                     passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                 print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Getting second Passing Yards player data
#                 try:
#                     passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

#                 try:
#                     passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
#                 except NoSuchElementException:
#                     passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
#                 print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

#                 try:
#                     click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
#                 except NoSuchElementException:
#                     click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
#                 click_passing_yard_team_two_player_name.click()

#                 time.sleep(5)

#                 try:
#                     passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                 print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Rushing Yards
#                 try:
#                     rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
#                 except NoSuchElementException:
#                     rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
#                 print(f"rushing Yards : {rushing_yard_text}")

#                 try:
#                     rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

#                 try:
#                     rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                 except NoSuchElementException:
#                     rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

#                 try:
#                     click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
#                 except NoSuchElementException:
#                     click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
#                 click_rushing_yard_team_one_player_name.click()

#                 time.sleep(5)

#                 try:
#                     rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                 print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Getting second rushing Yards player data
#                 try:
#                     rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

#                 try:
#                     rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                 except NoSuchElementException:
#                     rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

#                 try:
#                     click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
#                 except NoSuchElementException:
#                     click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
#                 click_rushing_yard_team_two_player_name.click()

#                 time.sleep(5)

#                 try:
#                     rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                 print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Receiving Yards
#                 try:
#                     receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
#                 except NoSuchElementException:
#                     receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
#                 print(f"Receiving Yards : {receiving_yard_text}")

#                 try:
#                     receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

#                 try:
#                     receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                 except NoSuchElementException:
#                     receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

#                 try:
#                     click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
#                 except NoSuchElementException:
#                     click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
#                 click_receiving_yard_team_one_player_name.click()

#                 time.sleep(5)

#                 try:
#                     receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                 print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Getting second receiving Yards player data
#                 try:
#                     receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                 except NoSuchElementException:
#                     receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

#                 try:
#                     receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                 except NoSuchElementException:
#                     receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

#                 try:
#                     click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
#                 except NoSuchElementException:
#                     click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
#                 click_receiving_yard_team_two_player_name.click()

#                 time.sleep(5)

#                 try:
#                     receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                 except NoSuchElementException:
#                     receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
#                     receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                 print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

#                 # Go back to the Match page
#                 driver.back()

#                 # Team Stats
#                 try:
#                     team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
#                 except NoSuchElementException:
#                     team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
#                 print(f"Team One Total Yards States : {team_one_total_yards_states}")

#                 try:
#                     total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
#                 except NoSuchElementException:
#                     total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
#                 print(f"Team Two Total Yards States : {total_yards_states}")

#                 try:
#                     team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
#                 except NoSuchElementException:
#                     team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
#                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")

#                 # Turnovers
#                 try:
#                     team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
#                 except NoSuchElementException:
#                     team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
#                 print(f"Team One Turnovers States : {team_one_turnovers_states}")

#                 try:
#                     turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
#                 except NoSuchElementException:
#                     turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
#                 print(f"Team One Total Yards States : {turnovers_states}")
                
#                 try:
#                     team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
#                 except NoSuchElementException:
#                     team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
#                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")

#                 # 1st Downs
#                 try:
#                     team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
#                 except NoSuchElementException:
#                     team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
#                 print(f"Team One first_downs States : {team_one_first_downs_states}")

#                 try:
#                     first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
#                 except NoSuchElementException:
#                     first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
#                 print(f"Team One Total 1st Downs States : {first_downs_states}")
                
#                 try:
#                     team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
#                 except NoSuchElementException:
#                     team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
#                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                
#                 # Time of Possession
#                 try:
#                     team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
#                 except NoSuchElementException:
#                     team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
#                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

#                 try:
#                     time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
#                 except NoSuchElementException:
#                     time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
#                 print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                
#                 try:
#                     team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
#                 except NoSuchElementException:
#                     team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
#                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

#                 driver.back()

#             else: 
#                 continue
            
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     driver.quit()

# finally:
#     csv_file.close()
#     driver.quit()














import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
time.sleep(5)

# --- CSV SETUP ---
final_headers = ["team_1_score", "team_1_records", "team_2_records", "team_1_game_state", "team_2_game_state", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
                 "pass_p1_img", "pass_p2_name", "pass_p2_stats","pass_p2_img", "rush_p1_name", "rush_p1_stats",
                 "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
                 "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards"
]

# Open the CSV file and write the headers
final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
final_csv_writer = csv.writer(final_csv_file)
final_csv_writer.writerow(final_headers)

live_headers = ["team_1_name", "team_1_records", "team_1_score", "team_2_name", "team_2_records", "team_2_score", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
                "pass_p1_img", "pass_p2_name", "pass_p2_stats", "pass_p2_img", "rush_p1_name", "rush_p1_stats",
                "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
                "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", "team_1_first_downs", 
                "team_2_first_downs", "team_1_time_possession", "team_2_time_possession"
]


# Open the CSV file and write the headers
live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
live_csv_writer = csv.writer(live_csv_file)
live_csv_writer.writerow(live_headers)


finished_games = []

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
            if game_id not in finished_games:

                if game_status == "FINAL":
                    try:
                        print("Scraping a FINAL game.")
                        click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
                        click_gamecast_button.click()
                        # Add the game ID to the list to prevent future scraping
                        finished_games.append(game_id)
                    except NoSuchElementException:
                        print("Click Gamecast button not found.")
                        continue

                    time.sleep(5)

                    team_one_name_xpath = "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2"
        
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, team_one_name_xpath))
                    )
                    
                    team_one_name = driver.find_element(By.XPATH, team_one_name_xpath).text
                    print(f"Team 1 Name: {team_one_name}")
                    

                    try:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    print(f"Stat: {team_one_score}")

                    try:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    except NoSuchElementException:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    print(f"Team 1 Records: {team_one_records}")

                    try:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    except NoSuchElementException:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    print(f"Team 2 Records: {team_two_records}")

                    try:
                        team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    except NoSuchElementException:
                        team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    print(f"Team One state: {team_one_game_state}")

                    try:
                        team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    except NoSuchElementException:
                        team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    print(f"Team Two Stat: {team_two_game_state}")

                    try:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    print(f"Team 1 Logo: {team_one_image}")

                    try:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    print(f"Team 2 Logo: {team_two_image}")

                    #Passing Yards
                    try:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                    try:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                    time.sleep(2)
                    try:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                    except NoSuchElementException:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                    click_passing_yard_team_one_player_name.click()

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
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                    try:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                    print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                    except NoSuchElementException:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                    click_passing_yard_team_two_player_name.click()

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
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                    try:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")


                    time.sleep(2)
                    try:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                    except NoSuchElementException:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                    click_rushing_yard_team_one_player_name.click()

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
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                    try:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                    except NoSuchElementException:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                    click_rushing_yard_team_two_player_name.click()

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
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                    try:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                    time.sleep(2)
                    try:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                    except NoSuchElementException:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                    click_receiving_yard_team_one_player_name.click()

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
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                    try:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                    time.sleep(2)
                    try:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                    except NoSuchElementException:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                    click_receiving_yard_team_two_player_name.click()

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
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                    try:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                    # Turnovers
                    try:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                    print(f"Team One Turnovers States : {team_one_turnovers_states}")

                    try:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
                    except NoSuchElementException:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
                    print(f"Team One Total Yards States : {turnovers_states}")
                    
                    try:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                    # 1st Downs
                    try:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                    print(f"Team One first_downs States : {team_one_first_downs_states}")

                    try:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
                    except NoSuchElementException:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
                    print(f"Team One Total 1st Downs States : {first_downs_states}")
                    
                    try:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
                    # Time of Possession
                    try:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                    except NoSuchElementException:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

                    try:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
                    except NoSuchElementException:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
                    print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                    
                    try:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                    except NoSuchElementException:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

                    click_receiving_yard_team_two_player_name

                    final_data = [team_one_name, team_one_score, team_one_records, team_two_records, team_one_game_state, team_two_game_state, team_one_image, team_two_image, 
                                  passing_yard_team_one_player_name, passing_yard_team_one_player_states,
                                  passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
                                  passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
                                  rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
                                  rushing_yard_team_two_player_name, rushing_yard_team_two_player_states,
                                  rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
                                  receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
                                  receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
                                  team_one_total_yards_states, team_two_total_yards_states]
                    
                    final_csv_writer.writerow(final_data)
                    
                    driver.back()

                elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
                    # --- SCRAPING AND PRINTING ALL LIVE DATA ---
                    print("----------------------------------------")
                    print(f"Game is still in progress: {game_status}")

                    try:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                    except NoSuchElementException:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

                    try:
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text                                  
                    except NoSuchElementException:
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    print(f"Team One Name: {team_one_name}")

                    # try:
                    #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    # except NoSuchElementException:
                    #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    # print(f"Team One : {team_one_score}")

                    try:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    except NoSuchElementException:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    print(f"Team 1 Records: {team_one_records}")

                    try:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                    print(f"Team One Live Score: {team_one_live_score}")

                    try:
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    except NoSuchElementException:
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    print(f"Team Two Name: {team_two_name}")

                    try:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    except NoSuchElementException:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    print(f"Team 2 Records: {team_two_records}")

                    try:
                        team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                    print(f"Team Two Live Score: {team_two_live_score}")

                    try:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    print(f"Team 1 Logo: {team_one_image}")

                    try:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    print(f"Team 2 Logo: {team_two_image}")

                    #Passing Yards

                    try:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                    try:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                    time.sleep(5)
                    try:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                    except NoSuchElementException:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                    click_passing_yard_team_one_player_name.click()

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
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

                    try:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
                    print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

                    try:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
                    except NoSuchElementException:
                        click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
                    click_passing_yard_team_two_player_name.click()

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
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

                    try:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
                    print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

                    try:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
                    except NoSuchElementException:
                        click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
                    click_rushing_yard_team_one_player_name.click()

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
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

                    try:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
                    print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

                    try:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
                    except NoSuchElementException:
                        click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
                    click_rushing_yard_team_two_player_name.click()

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
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

                    try:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
                    print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

                    try:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
                    except NoSuchElementException:
                        click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
                    click_receiving_yard_team_one_player_name.click()

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
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
                    print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

                    try:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    except NoSuchElementException:
                        receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
                    print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

                    try:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
                    except NoSuchElementException:
                        click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
                    click_receiving_yard_team_two_player_name.click()

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
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                    try:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                    # Turnovers
                    try:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                    print(f"Team One Turnovers States : {team_one_turnovers_states}")
                    
                    try:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                    # 1st Downs
                    try:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                    print(f"Team One first_downs States : {team_one_first_downs_states}")
                    
                    try:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
                    # Time of Possession
                    try:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                    except NoSuchElementException:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                    
                    try:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                    except NoSuchElementException:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
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
            else:
                print(f"Game with ID {game_id} already scraped. Skipping.")
            
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    driver.quit()

finally:
    final_csv_file.close()
    live_csv_file.close()
    driver.quit()






import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- SETUP ---
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
time.sleep(5)

# --- CSV SETUP ---
final_headers = ["team_1_score", "team_1_records", "team_2_records", "team_1_game_state", "team_2_game_state", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
                 "pass_p1_img", "pass_p2_name", "pass_p2_stats","pass_p2_img", "rush_p1_name", "rush_p1_stats",
                 "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
                 "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards"
]

# Open the CSV file and write the headers
final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
final_csv_writer = csv.writer(final_csv_file)
final_csv_writer.writerow(final_headers)

live_headers = ["team_1_name", "team_1_records", "team_1_score", "team_2_name", "team_2_records", "team_2_score", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
                "pass_p1_img", "pass_p2_name", "pass_p2_stats", "pass_p2_img", "rush_p1_name", "rush_p1_stats",
                "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
                "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", "team_1_first_downs", 
                "team_2_first_downs", "team_1_time_possession", "team_2_time_possession"
]


# Open the CSV file and write the headers
live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
live_csv_writer = csv.writer(live_csv_file)
live_csv_writer.writerow(live_headers)


finished_games = []

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
            if game_id not in finished_games:

                if game_status == "FINAL":
                    try:
                        print("Scraping a FINAL game.")
                        click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
                        click_gamecast_button.click()
                        # Add the game ID to the list to prevent future scraping
                        finished_games.append(game_id)
                    except NoSuchElementException:
                        print("Click Gamecast button not found.")
                        continue

                    time.sleep(5)

                    team_one_name_xpath = "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2"
        
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, team_one_name_xpath))
                    )
                    
                    team_one_name = driver.find_element(By.XPATH, team_one_name_xpath).text
                    print(f"Team 1 Name: {team_one_name}")
                    

                    try:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    print(f"Stat: {team_one_score}")

                    try:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    except NoSuchElementException:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    print(f"Team 1 Records: {team_one_records}")

                    try:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    except NoSuchElementException:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    print(f"Team 2 Records: {team_two_records}")

                    try:
                        team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    except NoSuchElementException:
                        team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
                    print(f"Team One state: {team_one_game_state}")

                    try:
                        team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    except NoSuchElementException:
                        team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
                    print(f"Team Two Stat: {team_two_game_state}")

                    try:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    print(f"Team 1 Logo: {team_one_image}")

                    try:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    print(f"Team 2 Logo: {team_two_image}")

                    #Passing Yards
                    try:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
                    print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

                    try:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    except NoSuchElementException:
                        passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
                    print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

                    time.sleep(2)
                    try:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
                    except NoSuchElementException:
                        click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
                    click_passing_yard_team_one_player_name.click()

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
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                    try:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                    # Turnovers
                    try:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                    print(f"Team One Turnovers States : {team_one_turnovers_states}")

                    try:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
                    except NoSuchElementException:
                        turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
                    print(f"Team One Total Yards States : {turnovers_states}")
                    
                    try:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                    # 1st Downs
                    try:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                    print(f"Team One first_downs States : {team_one_first_downs_states}")

                    try:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
                    except NoSuchElementException:
                        first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
                    print(f"Team One Total 1st Downs States : {first_downs_states}")
                    
                    try:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
                    # Time of Possession
                    try:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                    except NoSuchElementException:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

                    try:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
                    except NoSuchElementException:
                        time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
                    print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                    
                    try:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                    except NoSuchElementException:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
                    print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

                    click_receiving_yard_team_two_player_name

                    final_data = [team_one_name, team_one_score, team_one_records, team_two_records, team_one_game_state, team_two_game_state, team_one_image, team_two_image, 
                                  passing_yard_team_one_player_name, passing_yard_team_one_player_states,
                                  passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
                                  passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
                                  rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
                                  rushing_yard_team_two_player_name, rushing_yard_team_two_player_states,
                                  rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
                                  receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
                                  receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
                                  team_one_total_yards_states, team_two_total_yards_states]
                    
                    final_csv_writer.writerow(final_data)
                    
                    driver.back()

                elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
                    # --- SCRAPING AND PRINTING ALL LIVE DATA ---
                    print("----------------------------------------")
                    print(f"Game is still in progress: {game_status}")

                    try:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
                    except NoSuchElementException:
                        click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
                        click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

                    try:
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text                                  
                    except NoSuchElementException:
                        team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    print(f"Team One Name: {team_one_name}")

                    # try:
                    #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    # except NoSuchElementException:
                    #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
                    # print(f"Team One : {team_one_score}")

                    try:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    except NoSuchElementException:
                        team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
                        team_one_records = team_one_records.replace(" Away", "")
                    print(f"Team 1 Records: {team_one_records}")

                    try:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
                    print(f"Team One Live Score: {team_one_live_score}")

                    try:
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    except NoSuchElementException:
                        team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
                    print(f"Team Two Name: {team_two_name}")

                    try:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    except NoSuchElementException:
                        team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
                        team_two_records = team_two_records.replace(" Home", "")
                    print(f"Team 2 Records: {team_two_records}")

                    try:
                        team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                    except NoSuchElementException:
                        team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
                    print(f"Team Two Live Score: {team_two_live_score}")

                    try:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
                        team_one_image = team_one_image_script.get_attribute('src')
                    print(f"Team 1 Logo: {team_one_image}")

                    try:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
                    except NoSuchElementException:
                        team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
                        team_two_image = team_two_image_script.get_attribute('src')
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
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
                    print(f"Team One Total Yards States : {team_one_total_yards_states}")

                    try:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_total_yards_states}")

                    # Turnovers
                    try:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
                    print(f"Team One Turnovers States : {team_one_turnovers_states}")
                    
                    try:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
                    print(f"Team Two Total Yards States : {team_two_turnovers_states}")

                    # 1st Downs
                    try:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
                    except NoSuchElementException:
                        team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
                    print(f"Team One first_downs States : {team_one_first_downs_states}")
                    
                    try:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
                    except NoSuchElementException:
                        team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
                    print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
                    # Time of Possession
                    try:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
                    except NoSuchElementException:
                        team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
                    print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                    
                    try:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
                    except NoSuchElementException:
                        team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
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
            else:
                print(f"Game with ID {game_id} already scraped. Skipping.")
            
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    driver.quit()

finally:
    final_csv_file.close()
    live_csv_file.close()
    driver.quit()


