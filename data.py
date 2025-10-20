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













# # import time
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.common.exceptions import NoSuchElementException
# # import csv
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # # --- SETUP ---
# # chrome_options = Options()
# # chrome_options.add_experimental_option("detach", True)
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# # driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# # time.sleep(5)

# # # --- CSV SETUP ---
# # headers = [
# #     'Team One Name', 'Team One Score', 'Team One Location', 'Team One Logo',
# #     'Team Two Name', 'Team Two Score', 'Team Two Logo', 'Game Status',
# #     'Team One Scores by Quarter', 'Team Two Scores by Quarter',
# #     'Passing Yard Stat Name', 'Passing Yard Player One Image', 'Passing Yard Player One Team', 'Passing Yard Player One Name', 'Passing Yard Player One Stats',
# #     'Passing Yard Player Two Image', 'Passing Yard Player Two Team', 'Passing Yard Player Two Name', 'Passing Yard Player Two Stats',
# #     'Rushing Yard Stat Name', 'Rushing Yard Player One Image', 'Rushing Yard Player One Team', 'Rushing Yard Player One Name', 'Rushing Yard Player One Stats',
# #     'Rushing Yard Player Two Image', 'Rushing Yard Player Two Team', 'Rushing Yard Player Two Name', 'Rushing Yard Player Two Stats',
# #     'Receiving Yard Stat Name', 'Receiving Yard Player One Image', 'Receiving Yard Player One Team', 'Receiving Yard Player One Name', 'Receiving Yard Player One Stats',
# #     'Receiving Yard Player Two Image', 'Receiving Yard Player Two Team', 'Receiving Yard Player Two Name', 'Receiving Yard Player Two Stats',
# #     'Total Yards Team One', 'Total Yards Team Two',
# #     'Turnovers Team One', 'Turnovers Team Two',
# #     'First Downs Team One', 'First Downs Team Two'
# # ]

# # csv_file = open('nfl_games.csv', 'w', newline='', encoding='utf-8')
# # csv_writer = csv.writer(csv_file)
# # csv_writer.writerow(headers)


# # finished_games = []

# # # --- MAIN LOOP FOR SCRAPING EACH GAME ---
# # try:
# #     game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
# #     num_games = len(game_sections)
# #     print(f"The number of games found is: {num_games}")

# #     for i in range(num_games):
# #         games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
# #         number_of_games_in_day = len(games_in_day)
# #         print(f"Day {i+1}: The number of games is: {number_of_games_in_day}")

# #         for j in range(number_of_games_in_day): 
# #             try:
# #                 game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
# #                 game_status = driver.find_element(By.XPATH, game_status_xpath).text
# #             except NoSuchElementException:
# #                 game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
# #                 game_status = driver.find_element(By.XPATH, game_status_xpath).text
            
# #             # --- CODE TO ADD ---
# #             # Get the Gamecast URL and extract the unique game ID
# #             try:
# #                 gamecast_link_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
# #                 gamecast_url = gamecast_link_element.get_attribute('href')
# #                 game_id = gamecast_url.split('/')[-1]
# #             except NoSuchElementException:
# #                 # Handle cases where the gamecast link might not be available
# #                 print("Gamecast link not found.")
# #                 continue

# #             if game_id not in finished_games: 
# #                 # Add the game ID to the list to prevent future scraping
# #                 finished_games.append(game_id)
                
# #                 if game_status == "FINAL":
# #                     try:
# #                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
# #                     except NoSuchElementException:
# #                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

# #                     time.sleep(5)

# #                     team_one_name_xpath = "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2"
        
# #                     WebDriverWait(driver, 10).until(
# #                         EC.visibility_of_element_located((By.XPATH, team_one_name_xpath))
# #                     )
                    
# #                     team_one_name = driver.find_element(By.XPATH, team_one_name_xpath).text
# #                     print(f"Team 1 Name: {team_one_name}")
                    

# #                     try:
# #                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                     except NoSuchElementException:
# #                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                     print(f"Stat: {team_one_score}")

# #                     try:
# #                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                         team_one_records = team_one_records.replace(" Away", "")
# #                     except NoSuchElementException:
# #                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                         team_one_records = team_one_records.replace(" Away", "")
# #                     print(f"Team 1 Records: {team_one_records}")

# #                     try:
# #                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                         team_two_records = team_two_records.replace(" Home", "")
# #                     except NoSuchElementException:
# #                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                         team_two_records = team_two_records.replace(" Home", "")
# #                     print(f"Team 2 Records: {team_two_records}")

# #                     try:
# #                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                     except NoSuchElementException:
# #                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                     print(f"Stat: {team_one_live_score}")

# #                     try:
# #                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                     except NoSuchElementException:
# #                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                     print(f"Stat: {team_one_live_score}")

# #                     try:
# #                         team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                         team_one_image = team_one_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                         team_one_image = team_one_image_script.get_attribute('src')
# #                     print(f"Team 1 Logo: {team_one_image}")

# #                     try:
# #                         team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                         team_two_image = team_two_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                         team_two_image = team_two_image_script.get_attribute('src')
# #                     print(f"Team 2 Logo: {team_two_image}")

# #                     #Passing Yards
# #                     try:
# #                         passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
# #                     except NoSuchElementException:
# #                         passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
# #                     print(f"Passing Yards : {passing_yard_text}")

# #                     try:
# #                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

# #                     try:
# #                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                     except NoSuchElementException:
# #                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                     print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

# #                     time.sleep(2)
# #                     try:
# #                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
# #                     except NoSuchElementException:
# #                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
# #                     click_passing_yard_team_one_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                     print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     # Getting second Passing Yards player data
# #                     try:
# #                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                     print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

# #                     try:
# #                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
# #                     except NoSuchElementException:
# #                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
# #                     print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

# #                     time.sleep(2)
# #                     try:
# #                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
# #                     except NoSuchElementException:
# #                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
# #                     click_passing_yard_team_two_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                     print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     # Rushing Yards
# #                     try:
# #                         rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
# #                     except NoSuchElementException:
# #                         rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
# #                     print(f"rushing Yards : {rushing_yard_text}")

# #                     try:
# #                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

# #                     try:
# #                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                     except NoSuchElementException:
# #                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                     print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")


# #                     time.sleep(2)
# #                     try:
# #                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
# #                     except NoSuchElementException:
# #                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
# #                     click_rushing_yard_team_one_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                     print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     # Getting second rushing Yards player data
# #                     try:
# #                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                     print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

# #                     try:
# #                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                     except NoSuchElementException:
# #                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                     print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

# #                     time.sleep(2)
# #                     try:
# #                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
# #                     except NoSuchElementException:
# #                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
# #                     click_rushing_yard_team_two_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                     print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     # Receiving Yards
# #                     try:
# #                         receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
# #                     except NoSuchElementException:
# #                         receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
# #                     print(f"Receiving Yards : {receiving_yard_text}")

# #                     try:
# #                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                     print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

# #                     try:
# #                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                     except NoSuchElementException:
# #                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                     print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

# #                     time.sleep(2)
# #                     try:
# #                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
# #                     except NoSuchElementException:
# #                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
# #                     click_receiving_yard_team_one_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                     print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     # Getting second receiving Yards player data
# #                     try:
# #                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                     except NoSuchElementException:
# #                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                     print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

# #                     try:
# #                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                     except NoSuchElementException:
# #                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                     print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

# #                     time.sleep(2)
# #                     try:
# #                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
# #                     except NoSuchElementException:
# #                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
# #                     click_receiving_yard_team_two_player_name.click()

# #                     time.sleep(2)

# #                     try:
# #                         receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                     except NoSuchElementException:
# #                         receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                     print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

# #                     # Go back to the Match page
# #                     driver.back()

# #                     time.sleep(3)
# #                     # Team Stats
# #                     try:
# #                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
# #                     except NoSuchElementException:
# #                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
# #                     print(f"Team One Total Yards States : {team_one_total_yards_states}")

# #                     try:
# #                         total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
# #                     except NoSuchElementException:
# #                         total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
# #                     print(f"Team Two Total Yards States : {total_yards_states}")

# #                     try:
# #                         team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
# #                     except NoSuchElementException:
# #                         team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
# #                     print(f"Team Two Total Yards States : {team_two_total_yards_states}")

# #                     # Turnovers
# #                     try:
# #                         team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
# #                     except NoSuchElementException:
# #                         team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
# #                     print(f"Team One Turnovers States : {team_one_turnovers_states}")

# #                     try:
# #                         turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
# #                     except NoSuchElementException:
# #                         turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
# #                     print(f"Team One Total Yards States : {turnovers_states}")
                    
# #                     try:
# #                         team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
# #                     except NoSuchElementException:
# #                         team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
# #                     print(f"Team Two Total Yards States : {team_two_turnovers_states}")

# #                     # 1st Downs
# #                     try:
# #                         team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
# #                     except NoSuchElementException:
# #                         team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
# #                     print(f"Team One first_downs States : {team_one_first_downs_states}")

# #                     try:
# #                         first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
# #                     except NoSuchElementException:
# #                         first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
# #                     print(f"Team One Total 1st Downs States : {first_downs_states}")
                    
# #                     try:
# #                         team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
# #                     except NoSuchElementException:
# #                         team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
# #                     print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                    
# #                     # Time of Possession
# #                     try:
# #                         team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
# #                     except NoSuchElementException:
# #                         team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
# #                     print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

# #                     try:
# #                         time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
# #                     except NoSuchElementException:
# #                         time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
# #                     print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                    
# #                     try:
# #                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
# #                     except NoSuchElementException:
# #                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
# #                     print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                    
# #                     driver.back()

# #             elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
# #                 # --- SCRAPING AND PRINTING ALL LIVE DATA ---
# #                 print("----------------------------------------")
# #                 print(f"Game is still in progress: {game_status}")

# #                 try:
# #                     click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                     click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
# #                 except NoSuchElementException:
# #                     click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                     click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

# #                 try:
# #                     team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
                                                                   
# #                 except NoSuchElementException:
# #                     team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                 print(f"Stat: {team_one_name}")

# #                 try:
# #                     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                 except NoSuchElementException:
# #                     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                 print(f"Stat: {team_one_score}")

# #                 try:
# #                     team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                     team_one_records = team_one_records.replace(" Away", "")
# #                 except NoSuchElementException:
# #                     team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                     team_one_records = team_one_records.replace(" Away", "")
# #                 print(f"Team 1 Records: {team_one_records}")

# #                 try:
# #                     team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                     team_two_records = team_two_records.replace(" Home", "")
# #                 except NoSuchElementException:
# #                     team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                     team_two_records = team_two_records.replace(" Home", "")
# #                 print(f"Team 2 Records: {team_two_records}")

# #                 try:
# #                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                 except NoSuchElementException:
# #                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                 print(f"Stat: {team_one_live_score}")

# #                 try:
# #                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                 except NoSuchElementException:
# #                     team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                 print(f"Stat: {team_one_live_score}")

# #                 try:
# #                     team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                     team_one_image = team_one_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                     team_one_image = team_one_image_script.get_attribute('src')
# #                 print(f"Team 1 Logo: {team_one_image}")

# #                 try:
# #                     team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                     team_two_image = team_two_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                     team_two_image = team_two_image_script.get_attribute('src')
# #                 print(f"Team 2 Logo: {team_two_image}")

# #                 #Passing Yards
# #                 try:
# #                     passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/header").text
# #                 except NoSuchElementException:
# #                     passing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/header").text
# #                 print(f"Passing Yards : {passing_yard_text}")

# #                 try:
# #                     passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

# #                 try:
# #                     passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                 except NoSuchElementException:
# #                     passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

# #                 try:
# #                     click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
# #                 except NoSuchElementException:
# #                     click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[1]/section/div/div[2]/div[1]/section/div/a[1]")
# #                 click_passing_yard_team_one_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     passing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                 print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Getting second Passing Yards player data
# #                 try:
# #                     passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

# #                 try:
# #                     passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
# #                 except NoSuchElementException:
# #                     passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
# #                 print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

# #                 try:
# #                     click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
# #                 except NoSuchElementException:
# #                     click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
# #                 click_passing_yard_team_two_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     passing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                 print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Rushing Yards
# #                 try:
# #                     rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/header").text
# #                 except NoSuchElementException:
# #                     rushing_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/header").text
# #                 print(f"rushing Yards : {rushing_yard_text}")

# #                 try:
# #                     rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

# #                 try:
# #                     rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                 except NoSuchElementException:
# #                     rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

# #                 try:
# #                     click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
# #                 except NoSuchElementException:
# #                     click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
# #                 click_rushing_yard_team_one_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     rushing_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                 print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Getting second rushing Yards player data
# #                 try:
# #                     rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

# #                 try:
# #                     rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                 except NoSuchElementException:
# #                     rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

# #                 try:
# #                     click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
# #                 except NoSuchElementException:
# #                     click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
# #                 click_rushing_yard_team_two_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     rushing_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                 print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Receiving Yards
# #                 try:
# #                     receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/header").text
# #                 except NoSuchElementException:
# #                     receiving_yard_text = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/header").text
# #                 print(f"Receiving Yards : {receiving_yard_text}")

# #                 try:
# #                     receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

# #                 try:
# #                     receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                 except NoSuchElementException:
# #                     receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

# #                 try:
# #                     click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
# #                 except NoSuchElementException:
# #                     click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
# #                 click_receiving_yard_team_one_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     receiving_yard_team_one_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                 print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Getting second receiving Yards player data
# #                 try:
# #                     receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                 except NoSuchElementException:
# #                     receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

# #                 try:
# #                     receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                 except NoSuchElementException:
# #                     receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

# #                 try:
# #                     click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
# #                 except NoSuchElementException:
# #                     click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
# #                 click_receiving_yard_team_two_player_name.click()

# #                 time.sleep(5)

# #                 try:
# #                     receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                 except NoSuchElementException:
# #                     receiving_yard_team_two_player_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img")
# #                     receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                 print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")

# #                 # Go back to the Match page
# #                 driver.back()

# #                 # Team Stats
# #                 try:
# #                     team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
# #                 except NoSuchElementException:
# #                     team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
# #                 print(f"Team One Total Yards States : {team_one_total_yards_states}")

# #                 try:
# #                     total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/span").text
# #                 except NoSuchElementException:
# #                     total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/span").text
# #                 print(f"Team Two Total Yards States : {total_yards_states}")

# #                 try:
# #                     team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
# #                 except NoSuchElementException:
# #                     team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
# #                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")

# #                 # Turnovers
# #                 try:
# #                     team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
# #                 except NoSuchElementException:
# #                     team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
# #                 print(f"Team One Turnovers States : {team_one_turnovers_states}")

# #                 try:
# #                     turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/span").text
# #                 except NoSuchElementException:
# #                     turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/span").text
# #                 print(f"Team One Total Yards States : {turnovers_states}")
                
# #                 try:
# #                     team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
# #                 except NoSuchElementException:
# #                     team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
# #                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")

# #                 # 1st Downs
# #                 try:
# #                     team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
# #                 except NoSuchElementException:
# #                     team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
# #                 print(f"Team One first_downs States : {team_one_first_downs_states}")

# #                 try:
# #                     first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
# #                 except NoSuchElementException:
# #                     first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
# #                 print(f"Team One Total 1st Downs States : {first_downs_states}")
                
# #                 try:
# #                     team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
# #                 except NoSuchElementException:
# #                     team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
# #                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                
# #                 # Time of Possession
# #                 try:
# #                     team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
# #                 except NoSuchElementException:
# #                     team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
# #                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

# #                 try:
# #                     time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/span").text
# #                 except NoSuchElementException:
# #                     time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/span").text
# #                 print(f"Team One Total Time of Possession States : {time_of_possession_states}")
                
# #                 try:
# #                     team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
# #                 except NoSuchElementException:
# #                     team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
# #                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

# #                 driver.back()

# #             else: 
# #                 continue
            
# # except Exception as e:
# #     print(f"An unexpected error occurred: {e}")
# #     driver.quit()

# # finally:
# #     csv_file.close()
# #     driver.quit()














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
# from selenium.common.exceptions import TimeoutException

# # --- SETUP ---
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# time.sleep(5)

# # --- CSV SETUP ---
# final_headers = ["team_1_score", "team_1_records", "team_2_records", "team_1_game_state", "team_2_game_state", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
#                  "pass_p1_img", "pass_p2_name", "pass_p2_stats","pass_p2_img", "rush_p1_name", "rush_p1_stats",
#                  "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
#                  "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards"
# ]

# # Open the CSV file and write the headers
# final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
# final_csv_writer = csv.writer(final_csv_file)
# final_csv_writer.writerow(final_headers)

# live_headers = ["team_1_name", "team_1_records", "team_1_score", "team_2_name", "team_2_records", "team_2_score", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
#                 "pass_p1_img", "pass_p2_name", "pass_p2_stats", "pass_p2_img", "rush_p1_name", "rush_p1_stats",
#                 "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
#                 "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", "team_1_first_downs", 
#                 "team_2_first_downs", "team_1_time_possession", "team_2_time_possession"
# ]


# # Open the CSV file and write the headers
# live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
# live_csv_writer = csv.writer(live_csv_file)
# live_csv_writer.writerow(live_headers)


# finished_games = []

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

#             # The main check: if the game hasn't been scraped yet
#             if game_id not in finished_games:

#                 if game_status == "FINAL":
#                     try:
#                         print("Scraping a FINAL game.")
#                         click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
#                         click_gamecast_button.click()
#                         # Add the game ID to the list to prevent future scraping
#                         finished_games.append(game_id)
#                     except NoSuchElementException:
#                         print("Click Gamecast button not found.")
#                         continue

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
#                         team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     except NoSuchElementException:
#                         team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     print(f"Team One state: {team_one_game_state}")

#                     try:
#                         team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     except NoSuchElementException:
#                         team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     print(f"Team Two Stat: {team_two_game_state}")

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
#                         passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 1 Player Image not found within the given time.")
#                         passing_yard_team_one_player_image = "N/A"
                    
#                     # Navigate back to the gamecast page
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
#                         passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 2 Player Image not found within the given time.")
#                         passing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Rushing Yards
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
#                         rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 1 Player Image not found within the given time.")
#                         rushing_yard_team_one_player_image = "N/A"

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
#                         rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 2 Player Image not found within the given time.")
#                         rushing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Receiving Yards
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
#                         receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 1 Player Image not found within the given time.")
#                         receiving_yard_team_one_player_image = "N/A"

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
#                         receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 2 Player Image not found within the given time.")
#                         receiving_yard_team_two_player_image = "N/A"

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

#                     click_receiving_yard_team_two_player_name

#                     final_data = [team_one_name, team_one_score, team_one_records, team_two_records, team_one_game_state, team_two_game_state, team_one_image, team_two_image, 
#                                   passing_yard_team_one_player_name, passing_yard_team_one_player_states,
#                                   passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
#                                   passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
#                                   rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
#                                   rushing_yard_team_two_player_name, rushing_yard_team_two_player_states,
#                                   rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
#                                   receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
#                                   receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
#                                   team_one_total_yards_states, team_two_total_yards_states]
                    
#                     final_csv_writer.writerow(final_data)
                    
#                     driver.back()

#                 elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
#                     # --- SCRAPING AND PRINTING ALL LIVE DATA ---
#                     print("----------------------------------------")
#                     print(f"Game is still in progress: {game_status}")

#                     try:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
#                     except NoSuchElementException:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

#                     try:
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text                                  
#                     except NoSuchElementException:
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     print(f"Team One Name: {team_one_name}")

#                     # try:
#                     #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     # except NoSuchElementException:
#                     #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     # print(f"Team One : {team_one_score}")

#                     try:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     except NoSuchElementException:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     print(f"Team 1 Records: {team_one_records}")

#                     try:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
#                     except NoSuchElementException:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
#                     print(f"Team One Live Score: {team_one_live_score}")

#                     try:
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     except NoSuchElementException:
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     print(f"Team Two Name: {team_two_name}")

#                     try:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     except NoSuchElementException:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     print(f"Team 2 Records: {team_two_records}")

#                     try:
#                         team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
#                     except NoSuchElementException:
#                         team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
#                     print(f"Team Two Live Score: {team_two_live_score}")

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
#                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     except NoSuchElementException:
#                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                     print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

#                     try:
#                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                     except NoSuchElementException:
#                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                     print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

#                     time.sleep(5)
#                     try:
#                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
#                     click_passing_yard_team_one_player_name.click()

#                     time.sleep(5)

#                     try:
#                         passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 1 Player Image not found within the given time.")
#                         passing_yard_team_one_player_image = "N/A"

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

#                     try:
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
#                     click_passing_yard_team_two_player_name.click()

#                     time.sleep(5)

#                     try:
#                         passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 2 Player Image not found within the given time.")
#                         passing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Rushing Yards

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

#                     try:
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
#                     click_rushing_yard_team_one_player_name.click()

#                     time.sleep(5)

#                     try:
#                         rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 1 Player Image not found within the given time.")
#                         rushing_yard_team_one_player_image = "N/A"

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

#                     try:
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
#                     click_rushing_yard_team_two_player_name.click()

#                     time.sleep(5)

#                     try:
#                         rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 2 Player Image not found within the given time.")
#                         rushing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Receiving Yards

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

#                     try:
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
#                     except NoSuchElementException:
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
#                     click_receiving_yard_team_one_player_name.click()

#                     time.sleep(5)

#                     try:
#                         receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 1 Player Image not found within the given time.")
#                         receiving_yard_team_one_player_image = "N/A"

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

#                     try:
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
#                     except NoSuchElementException:
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
#                     click_receiving_yard_team_two_player_name.click()

#                     time.sleep(5)

#                     try:
#                         receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 2 Player Image not found within the given time.")
#                         receiving_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Team Stats
#                     try:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
#                     except NoSuchElementException:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
#                     print(f"Team One Total Yards States : {team_one_total_yards_states}")

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
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
#                     except NoSuchElementException:
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
#                     print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
    
#                     live_data = [team_one_name, team_one_records, team_one_live_score, team_two_name, team_two_records, team_two_live_score, team_one_image, 
#                                  team_two_image, passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
#                                  passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
#                                 passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
#                                  rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
#                                  rushing_yard_team_two_player_name, rushing_yard_team_two_player_states, 
#                                  rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states,
#                                receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
#                                  receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
#                                  team_one_total_yards_states, team_two_total_yards_states, team_one_turnovers_states, team_two_turnovers_states, 
#                                  team_one_first_downs_states, team_two_first_downs_states, team_one_time_of_possession_states, team_two_time_of_possession_states]

#                     live_csv_writer.writerow(live_data)
#                     driver.back()

#                 else:
#                     print(f"Game status is {game_status}. Skipping for now.")
#                     continue
#             else:
#                 print(f"Game with ID {game_id} already scraped. Skipping.")
            
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     driver.quit()

# finally:
#     final_csv_file.close()
#     live_csv_file.close()
#     driver.quit()






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
# from selenium.common.exceptions import TimeoutException

# # --- SETUP ---
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# time.sleep(5)

# # --- CSV SETUP ---
# final_headers = ["team_1_score", "team_1_records", "team_2_records", "team_1_game_state", "team_2_game_state", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
#                  "pass_p1_img", "pass_p2_name", "pass_p2_stats","pass_p2_img", "rush_p1_name", "rush_p1_stats",
#                  "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
#                  "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards"
# ]

# # Open the CSV file and write the headers
# final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
# final_csv_writer = csv.writer(final_csv_file)
# final_csv_writer.writerow(final_headers)

# live_headers = ["team_1_name", "team_1_records", "team_1_score", "team_2_name", "team_2_records", "team_2_score", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
#                 "pass_p1_img", "pass_p2_name", "pass_p2_stats", "pass_p2_img", "rush_p1_name", "rush_p1_stats",
#                 "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
#                 "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", "team_1_first_downs", 
#                 "team_2_first_downs", "team_1_time_possession", "team_2_time_possession"
# ]


# # Open the CSV file and write the headers
# live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
# live_csv_writer = csv.writer(live_csv_file)
# live_csv_writer.writerow(live_headers)


# finished_games = []

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

#             # The main check: if the game hasn't been scraped yet
#             if game_id not in finished_games:

#                 if game_status == "FINAL":
#                     try:
#                         print("Scraping a FINAL game.")
#                         click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
#                         click_gamecast_button.click()
#                         # Add the game ID to the list to prevent future scraping
#                         finished_games.append(game_id)
#                     except NoSuchElementException:
#                         print("Click Gamecast button not found.")
#                         continue

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
#                         team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     except NoSuchElementException:
#                         team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
#                     print(f"Team One state: {team_one_game_state}")

#                     try:
#                         team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     except NoSuchElementException:
#                         team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
#                     print(f"Team Two Stat: {team_two_game_state}")

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
#                         passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 1 Player Image not found within the given time.")
#                         passing_yard_team_one_player_image = "N/A"
                    
#                     # Navigate back to the gamecast page
#                     driver.back()

#                     # Getting second Passing Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
#                         print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_two_player_name = "N/A"
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
#                         print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_two_player_states = "N/A"
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
#                         click_passing_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
#                             click_passing_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(2)
#                     try:
#                         passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 2 Player Image not found within the given time.")
#                         passing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Rushing Yards
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                         print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_one_player_name = "N/A"
#                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                         print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_one_player_states = "N/A"
#                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
#                         click_rushing_yard_team_one_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
#                             click_rushing_yard_team_one_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass
                    
#                     time.sleep(2)
#                     try:
#                         rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 1 Player Image not found within the given time.")
#                         rushing_yard_team_one_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second rushing Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                         print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_two_player_name = "N/A"
#                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                         print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_two_player_states = "N/A"
#                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
#                         click_rushing_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
#                             click_rushing_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(2)
#                     try:
#                         rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 2 Player Image not found within the given time.")
#                         rushing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Receiving Yards
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                         print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_one_player_name = "N/A"
#                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                         print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_one_player_states = "N/A"
#                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
#                         click_receiving_yard_team_one_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
#                             click_receiving_yard_team_one_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(2)

#                     try:
#                         receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 1 Player Image not found within the given time.")
#                         receiving_yard_team_one_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second receiving Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                         print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_two_player_name = "N/A"
#                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                         print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_two_player_states = "N/A"
#                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
#                         click_receiving_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
#                             click_receiving_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(2)
#                     try:
#                         receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 2 Player Image not found within the given time.")
#                         receiving_yard_team_two_player_image = "N/A"

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

#                     click_receiving_yard_team_two_player_name

#                     final_data = [team_one_name, team_one_score, team_one_records, team_two_records, team_one_game_state, team_two_game_state, team_one_image, team_two_image, 
#                                   passing_yard_team_one_player_name, passing_yard_team_one_player_states,
#                                   passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
#                                   passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
#                                   rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
#                                   rushing_yard_team_two_player_name, rushing_yard_team_two_player_states,
#                                   rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
#                                   receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
#                                   receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
#                                   team_one_total_yards_states, team_two_total_yards_states]
                    
#                     final_csv_writer.writerow(final_data)
                    
#                     driver.back()

#                 elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
#                     # --- SCRAPING AND PRINTING ALL LIVE DATA ---
#                     print("----------------------------------------")
#                     print(f"Game is still in progress: {game_status}")

#                     try:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
#                     except NoSuchElementException:
#                         click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
#                         click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()

#                     try:
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text                                  
#                     except NoSuchElementException:
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     print(f"Team One Name: {team_one_name}")

#                     # try:
#                     #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     # except NoSuchElementException:
#                     #     team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
#                     # print(f"Team One : {team_one_score}")

#                     try:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     except NoSuchElementException:
#                         team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
#                         team_one_records = team_one_records.replace(" Away", "")
#                     print(f"Team 1 Records: {team_one_records}")

#                     try:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
#                     except NoSuchElementException:
#                         team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
#                     print(f"Team One Live Score: {team_one_live_score}")

#                     try:
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     except NoSuchElementException:
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
#                     print(f"Team Two Name: {team_two_name}")

#                     try:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     except NoSuchElementException:
#                         team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
#                         team_two_records = team_two_records.replace(" Home", "")
#                     print(f"Team 2 Records: {team_two_records}")

#                     try:
#                         team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
#                     except NoSuchElementException:
#                         team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
#                     print(f"Team Two Live Score: {team_two_live_score}")

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
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                         print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                             print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_one_player_name = "N/A"
#                             print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                         print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
#                             print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_one_player_name = "N/A"
#                             print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

#                     time.sleep(5)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
#                         click_passing_yard_team_one_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
#                             click_passing_yard_team_one_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)
#                     try:
#                         passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 1 Player Image not found within the given time.")
#                         passing_yard_team_one_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second Passing Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
#                         print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_two_player_name = "N/A"
#                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
#                         print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
#                             print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             passing_yard_team_two_player_states = "N/A"
#                             print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
#                         click_passing_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
#                             click_passing_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)
#                     try:
#                         passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Passing Yards Team 2 Player Image not found within the given time.")
#                         passing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Rushing Yards
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                         print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_one_player_name = "N/A"
#                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                         print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
#                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_one_player_states = "N/A"
#                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
#                         click_rushing_yard_team_one_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
#                             click_rushing_yard_team_one_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)
#                     try:
#                         rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 1 Player Image not found within the given time.")
#                         rushing_yard_team_one_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second rushing Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                         print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_two_player_name = "N/A"
#                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                         print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
#                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             rushing_yard_team_two_player_states = "N/A"
#                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
#                         click_rushing_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
#                             click_rushing_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)

#                     try:
#                         rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Rushing Yards Team 2 Player Image not found within the given time.")
#                         rushing_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Receiving Yards
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                         print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
#                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_one_player_name = "N/A"
#                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                         print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
#                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_one_player_name = "N/A"
#                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
#                         click_receiving_yard_team_one_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
#                             click_receiving_yard_team_one_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)

#                     try:
#                         receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 1 Player Image not found within the given time.")
#                         receiving_yard_team_one_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Getting second receiving Yards player data
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                         print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
#                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_two_player_name = "N/A"
#                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                         print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
#                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             receiving_yard_team_two_player_states = "N/A"
#                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

#                     time.sleep(2)
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
#                         click_receiving_yard_team_two_player_name.click()
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
#                             click_receiving_yard_team_two_player_name.click()
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             pass

#                     time.sleep(5)
#                     try:
#                         receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
#                             EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
#                         )
#                         receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
#                         print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
#                     except TimeoutException:
#                         print("Receiving Yards Team 2 Player Image not found within the given time.")
#                         receiving_yard_team_two_player_image = "N/A"

#                     # Go back to the Match page
#                     driver.back()

#                     # Team Stats
#                     try:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
#                     except NoSuchElementException:
#                         team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
#                     print(f"Team One Total Yards States : {team_one_total_yards_states}")

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
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
#                     except NoSuchElementException:
#                         team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
#                     print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
    
#                     live_data = [team_one_name, team_one_records, team_one_live_score, team_two_name, team_two_records, team_two_live_score, team_one_image, 
#                                  team_two_image, passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
#                                  passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
#                                 passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
#                                  rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
#                                  rushing_yard_team_two_player_name, rushing_yard_team_two_player_states, 
#                                  rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states,
#                                receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
#                                  receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
#                                  team_one_total_yards_states, team_two_total_yards_states, team_one_turnovers_states, team_two_turnovers_states, 
#                                  team_one_first_downs_states, team_two_first_downs_states, team_one_time_of_possession_states, team_two_time_of_possession_states]

#                     live_csv_writer.writerow(live_data)
#                     driver.back()

#                 else:
#                     print(f"Game status is {game_status}. Skipping for now.")
#                     continue
#             else:
#                 print(f"Game with ID {game_id} already scraped. Skipping.")
            
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     driver.quit()

# finally:
#     final_csv_file.close()
#     live_csv_file.close()
#     driver.quit()















# # import time
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.common.exceptions import NoSuchElementException
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException
# # import csv
# # import os
# # import datetime


# # # --- SETUP ---
# # chrome_options = Options()
# # chrome_options.add_experimental_option("detach", True)
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# # # driver.get("https://www.espn.com/nfl/scoreboard/_/week/4/year/2025/seasontype/1")
# # # time.sleep(5)

# # # Get the current date and time
# # current_date = datetime.date.today()
# # print(f"Current date: {current_date}")

# # # A dictionary to map each week to its start date (Thursday)
# # week_start_dates = {
# #     1: datetime.date(2025, 9, 4),
# #     2: datetime.date(2025, 9, 11),
# #     3: datetime.date(2025, 9, 18),
# #     4: datetime.date(2025, 9, 25),
# #     5: datetime.date(2025, 10, 2),
# #     6: datetime.date(2025, 10, 9),
# #     7: datetime.date(2025, 10, 16),
# #     8: datetime.date(2025, 10, 23),
# #     9: datetime.date(2025, 10, 30),
# #     10: datetime.date(2025, 11, 6),
# #     11: datetime.date(2025, 11, 13),
# #     12: datetime.date(2025, 11, 20),
# #     13: datetime.date(2025, 11, 27),
# #     14: datetime.date(2025, 12, 4),
# #     15: datetime.date(2025, 12, 11),
# #     16: datetime.date(2025, 12, 18),
# #     17: datetime.date(2025, 12, 25),
# #     18: datetime.date(2026, 1, 1),
# # }

# # # This is to keep track of already scraped games
# # scraped_file = 'scraped_games.txt'
# # scraped_game_ids = set()

# # if os.path.exists(scraped_file):
# #     with open(scraped_file, 'r') as f:
# #         for line in f:
# #             scraped_game_ids.add(line.strip())

# # # This is to keep track of which week has be scraped
# # scraped_weeks_file = 'scraped_weeks.txt'
# # scraped_weeks = set()

# # if os.path.exists(scraped_weeks_file):
# #     with open(scraped_weeks_file, 'r') as f:
# #         for line in f:
# #             # Convert the line from a string to an integer
# #             scraped_weeks.add(int(line.strip()))

# # # --- CSV SETUP ---
# # final_headers = [
# #     "team_1_name", "team_1_score", "team_1_records", 
# #     "team_2_name", "team_2_score", "team_2_records", 
# #     "team_1_game_state", "team_2_game_state", 
# #     "team_1_logo", "team_2_logo",
# #     "pass_p1_name", "pass_p1_stats", "pass_p1_img", 
# #     "pass_p2_name", "pass_p2_stats", "pass_p2_img",
# #     "rush_p1_name", "rush_p1_stats", "rush_p1_img", 
# #     "rush_p2_name", "rush_p2_stats", "rush_p2_img",
# #     "rec_p1_name", "rec_p1_stats", "rec_p1_img", 
# #     "rec_p2_name", "rec_p2_stats", "rec_p2_img",
# #     "team_1_total_yards", "team_2_total_yards"
# # ]

# # # Open the CSV file and write the headers
# # final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
# # final_csv_writer = csv.writer(final_csv_file)
# # final_csv_writer.writerow(final_headers)

# # live_headers = [
# #     "team_1_name", "team_1_records", "team_1_score", 
# #     "team_2_name", "team_2_records", "team_2_score", 
# #     "team_1_logo", "team_2_logo", "pass_p1_name", 
# #     "pass_p1_stats", "pass_p1_img", "pass_p2_name",
# #     "pass_p2_stats", "pass_p2_img", "rush_p1_name", 
# #     "rush_p1_stats", "rush_p1_img", "rush_p2_name", 
# #     "rush_p2_stats", "rush_p2_img", "rec_p1_name", 
# #     "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
# #     "rec_p2_stats", "rec_p2_img", "team_1_total_yards", 
# #     "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", 
# #     "team_1_first_downs","team_2_first_downs", "team_1_time_possession", 
# #     "team_2_time_possession"
# # ]


# # # Open the CSV file and write the headers
# # live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
# # live_csv_writer = csv.writer(live_csv_file)
# # live_csv_writer.writerow(live_headers)

# # # The base URL format string is now a regular string
# # base_url_format = "https://www.espn.com/nfl/scoreboard/_/week/{week}/year/2025/seasontype/2"

# # # Iterate through all 18 regular season weeks
# # for week_number in range(1, 19):
# #     # Check if the current week has started
# #     if week_start_dates.get(week_number) is None or week_start_dates[week_number] > current_date:
# #         print(f"Week {week_number} has not yet started. Stopping the program.")
# #         break
    
# #     # Check if the week has already been scraped
# #     if week_number in scraped_weeks:
# #         print(f"Week {week_number} already scraped. Skipping.")
# #         continue

# #     # Construct the full URL using the 'week_number' variable
# #     current_url = base_url_format.format(week=week_number)
# #     print(f"Navigating to: {current_url}")
# #     driver.get(current_url)
# #     time.sleep(5) 

# #     try:
# #         game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
# #         num_games = len(game_sections)
# #         print(f"The number of days found is: {num_games}")

# #         for i in range(num_games):
# #             games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
# #             number_of_games_in_day = len(games_in_day)
# #             print(f"Day {i+1}: The number of games is: {number_of_games_in_day}")

# #             for j in range(number_of_games_in_day):
# #                 try:
# #                     game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
# #                     game_status = driver.find_element(By.XPATH, game_status_xpath).text
# #                 except NoSuchElementException:
# #                     game_status_xpath = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[1]/div/div[1]/section/div/div/div[1]/div[1]"
# #                     game_status = driver.find_element(By.XPATH, game_status_xpath).text

# #                 # --- CODE TO ADD ---
# #                 # Get the Gamecast URL and extract the unique game ID
# #                 try:
# #                     gamecast_link_element = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
# #                     gamecast_url = gamecast_link_element.get_attribute('href')
# #                     game_id = gamecast_url.split('/')[-1]
# #                 except NoSuchElementException:
# #                     # Handle cases where the gamecast link might not be available
# #                     print("Gamecast link not found.")
# #                     continue

# #                 # The main check: if the game hasn't been scraped yet
# #                 if game_id in scraped_game_ids:
# #                     print(f"Game with ID {game_id} already scraped. Skipping.")
# #                     continue
# #                 else: 
# #                     if game_status == "FINAL":
# #                         try:
# #                             print("Scraping a FINAL game.")
# #                             click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
# #                             click_gamecast_button.click()
# #                         except NoSuchElementException:
# #                             print("Click Gamecast button not found.")
# #                             continue

# #                         time.sleep(5)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                             print(f"Team 1 Name: {team_one_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[1]/div/section[2]/div[1]/div/div[1]/section/div/div/ul/li[1]/div[1]/div[1]/a/div").text
# #                                 print(f"Team 1 Name: {team_one_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_name = "N/A"
# #                                 print(f"Team 1 Name: {team_one_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                             print(f"Team 1 Score: {team_one_score}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]").text
# #                                 print(f"Team 1 Score: {team_one_score}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_score = "N/A"
# #                                 print(f"Team 1 Score: {team_one_score}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                             team_one_records = team_one_records.replace(" Away", "")
# #                             print(f"Team 1 Records: {team_one_records}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").text
# #                                 team_one_records = team_one_records.replace(" Away", "")
# #                                 print(f"Team 1 Records: {team_one_records}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_records = "N/A"
# #                                 print(f"Team 1 Records: {team_one_records}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                             print(f"Team 2 Name: {team_two_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second two
# #                                 team_two_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                                 print(f"Team 2 Name: {team_two_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_name = "N/A"
# #                                 print(f"Team 2 Name: {team_two_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
# #                             print(f"Team 2 Score: {team_two_score}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second two
# #                                 team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
# #                                 print(f"Team 2 Score: {team_two_score}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_score = "N/A"
# #                                 print(f"Team 2 Score: {team_two_score}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                             team_two_records = team_two_records.replace(" Home", "")
# #                             print(f"Team 2 Records: {team_two_records}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[2]/div[2]").text
# #                                 team_two_records = team_two_records.replace(" Home", "")
# #                                 print(f"Team 2 Records: {team_two_records}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_records = "N/A"
# #                                 print(f"Team 2 Records: {team_two_records}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                             print(f"Team One state: {team_one_game_state}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[1]").text
# #                                 print(f"Team One state: {team_one_game_state}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_game_state = "N/A"
# #                                 print(f"Team One state: {team_one_game_state}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                             print(f"Team Two Stat: {team_two_game_state}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[2]").text
# #                                 print(f"Team Two Stat: {team_two_game_state}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_game_state = "N/A"
# #                                 print(f"Team Two Stat: {team_two_game_state}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                             team_one_image = team_one_image_script.get_attribute('src')
# #                             print(f"Team 1 Logo: {team_one_image}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                                 team_one_image = team_one_image_script.get_attribute('src')
# #                                 print(f"Team 1 Logo: {team_one_image}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_image = "N/A"
# #                                 print(f"Team 1 Logo: {team_one_image}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                             team_two_image = team_two_image_script.get_attribute('src')
# #                             print(f"Team 2 Logo: {team_two_image}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                                 team_two_image = team_two_image_script.get_attribute('src')
# #                                 print(f"Team 2 Logo: {team_two_image}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_image = "N/A"
# #                                 print(f"Team 2 Logo: {team_two_image}")

# #                         #Passing Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"//html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_one_player_name = "N/A"
# #                                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                             print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_one_player_states = "N/A"
# #                                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
# #                             click_passing_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
# #                                 click_passing_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(2)

# #                         try:
# #                             passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Passing Yards Team 1 Player Image not found within the given time.")
# #                             passing_yard_team_one_player_image = "N/A"
                        
# #                         # Navigate back to the gamecast page
# #                         driver.back()

# #                         # Getting second Passing Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
# #                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_two_player_name = "N/A"
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
# #                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_two_player_states = "N/A"
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
# #                             click_passing_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
# #                                 click_passing_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(2)
# #                         try:
# #                             passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Passing Yards Team 2 Player Image not found within the given time.")
# #                             passing_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Rushing Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_one_player_name = "N/A"
# #                                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_one_player_states = "N/A"
# #                                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
# #                             click_rushing_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
# #                                 click_rushing_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass
                        
# #                         time.sleep(2)
# #                         try:
# #                             rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Rushing Yards Team 1 Player Image not found within the given time.")
# #                             rushing_yard_team_one_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Getting second rushing Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_two_player_name = "N/A"
# #                                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_two_player_states = "N/A"
# #                                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
# #                             click_rushing_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
# #                                 click_rushing_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(2)
# #                         try:
# #                             rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Rushing Yards Team 2 Player Image not found within the given time.")
# #                             rushing_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Receiving Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_one_player_name = "N/A"
# #                                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_one_player_states = "N/A"
# #                                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
# #                             click_receiving_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
# #                                 click_receiving_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(2)

# #                         try:
# #                             receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Receiving Yards Team 1 Player Image not found within the given time.")
# #                             receiving_yard_team_one_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Getting second receiving Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_two_player_name = "N/A"
# #                                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_two_player_states = "N/A"
# #                                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
# #                             click_receiving_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
# #                                 click_receiving_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(2)
# #                         try:
# #                             receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Receiving Yards Team 2 Player Image not found within the given time.")
# #                             receiving_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         time.sleep(3)
# #                         # Team Stats
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
# #                             print(f"Team One Total Yards States : {team_one_total_yards_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[4]/section/div/div[2]/div[1]/span").text
# #                                 print(f"Team One Total Yards States : {team_one_total_yards_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_total_yards_states = "N/A"
# #                                 print(f"Team One Total Yards States : {team_one_total_yards_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
# #                             print(f"Team Two Total Yards States : {team_two_total_yards_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
# #                                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_total_yards_states = "N/A"
# #                                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")

# #                         # Turnovers
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
# #                             print(f"Team One Turnovers States : {team_one_turnovers_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
# #                                 print(f"Team One Turnovers States : {team_one_turnovers_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_total_yards_states = "N/A"
# #                                 print(f"Team One Turnovers States : {team_one_turnovers_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
# #                             print(f"Team Two Total Yards States : {team_two_turnovers_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
# #                                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_turnovers_states = "N/A"
# #                                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")

# #                         # 1st Downs
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
# #                             print(f"Team One first_downs States : {team_one_first_downs_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
# #                                 print(f"Team One first_downs States : {team_one_first_downs_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_first_downs_states = "N/A"
# #                                 print(f"Team One first_downs States : {team_one_first_downs_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/span").text
# #                             print(f"Team One Total 1st Downs States : {first_downs_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/span").text
# #                                 print(f"Team One Total 1st Downs States : {first_downs_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 first_downs_states = "N/A"
# #                                 print(f"Team One Total 1st Downs States : {first_downs_states}")
                        
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
# #                             print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
# #                                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_first_downs_states = "N/A"
# #                                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                        
# #                         # Time of Possession
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[1]").text
# #                             print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[1]").text
# #                                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_time_of_possession_states = "N/A"
# #                                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
                        
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[2]").text
# #                             print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[5]/section/div/div[5]/div/span[2]").text
# #                                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_time_of_possession_states = "N/A"
# #                                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")

# #                         click_receiving_yard_team_two_player_name

# #                         final_data = [
# #                             team_one_name, team_one_score, team_one_records, 
# #                             team_two_name, team_two_score, team_two_records, 
# #                             team_one_game_state, team_two_game_state, 
# #                             team_one_image, team_two_image, 
# #                             passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
# #                             passing_yard_team_one_player_image, passing_yard_team_two_player_name, 
# #                             passing_yard_team_two_player_states, passing_yard_team_two_player_image, 
# #                             rushing_yard_team_one_player_name, rushing_yard_team_one_player_states, 
# #                             rushing_yard_team_one_player_image, rushing_yard_team_two_player_name, 
# #                             rushing_yard_team_two_player_states, rushing_yard_team_two_player_image, 
# #                             receiving_yard_team_one_player_name, receiving_yard_team_one_player_states, 
# #                             receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
# #                             receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
# #                             team_one_total_yards_states, team_two_total_yards_states
# #                         ]
                        
# #                         final_csv_writer.writerow(final_data)

# #                         scraped_game_ids.add(game_id)
# #                         with open(scraped_file, 'a') as f:
# #                             f.write(game_id + '\n')
                        
# #                         driver.back()

# #                     elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
# #                         # --- SCRAPING AND PRINTING ALL LIVE DATA ---
# #                         print("----------------------------------------")
# #                         print(f"Game is still in progress: {game_status}")
                        
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                             click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_gamecast_button = f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]"
# #                                 click_gamecast_button = driver.find_element(By.XPATH, click_gamecast_button).click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                             print(f"Team One Name: {team_one_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                                 print(f"Team One Name: {team_one_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_name = "N/A"
# #                                 print(f"Team One Name: {team_one_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
# #                             print(f"Team 1 Records: {team_one_records}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]").text
# #                                 print(f"Team 1 Records: {team_one_records}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_records = "N/A"
# #                                 print(f"Team 1 Records: {team_one_records}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
# #                             print(f"Team One Live Score: {team_one_live_score}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]").text
# #                                 print(f"Team One Live Score: {team_one_live_score}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_live_score = "N/A"
# #                                 print(f"Team One Live Score: {team_one_live_score}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                             print(f"Team Two Name: {team_two_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[1]/div[2]/a/h2").text
# #                                 print(f"Team Two Name: {team_two_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_name = "N/A"
# #                                 print(f"Team Two Name: {team_two_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
# #                             team_two_records = team_two_records.replace(" Home", "")
# #                             print(f"Team 2 Records: {team_two_records}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_records = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]").text
# #                                 team_two_records = team_two_records.replace(" Home", "")
# #                                 print(f"Team 2 Records: {team_two_records}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_records = "N/A"
# #                                 print(f"Team 2 Records: {team_two_records}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
# #                             print(f"Team Two Live Score: {team_two_live_score}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_live_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div[1]").text
# #                                 print(f"Team Two Live Score: {team_two_live_score}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_live_score = "N/A"
# #                                 print(f"Team Two Live Score: {team_two_live_score}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                             team_one_image = team_one_image_script.get_attribute('src')
# #                             print(f"Team 1 Logo: {team_one_image}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/img")
# #                                 team_one_image = team_one_image_script.get_attribute('src')
# #                                 print(f"Team 1 Logo: {team_one_image}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_image = "N/A"
# #                                 print(f"Team 1 Logo: {team_one_image}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                             team_two_image = team_two_image_script.get_attribute('src')
# #                             print(f"Team 2 Logo: {team_two_image}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_image_script = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[1]/div[1]/div/div[2]/div[3]/div[1]/div[1]/div/img")
# #                                 team_two_image = team_two_image_script.get_attribute('src')
# #                                 print(f"Team 2 Logo: {team_two_image}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_image = "N/A"
# #                                 print(f"Team 2 Logo: {team_two_image}")

# #                         #Passing Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_one_player_name = "N/A"
# #                                 print(f"Passing Yards Team One Player Name: {passing_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                             print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[1]/div[2]").text
# #                                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_one_player_name = "N/A"
# #                                 print(f"Passing Yards Team One Player States : {passing_yard_team_one_player_states}")

# #                         time.sleep(5)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[3]/section/div/div[2]/div[1]/section/div/a[1]")
# #                             click_passing_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_passing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div/div[2]/section/div/div[2]/div[1]/section/div/a[1]")
# #                                 click_passing_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)
# #                         try:
# #                             passing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             passing_yard_team_one_player_image = passing_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"Passing Yards Team 1 Player Image: {passing_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Passing Yards Team 1 Player Image not found within the given time.")
# #                             passing_yard_team_one_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Getting second Passing Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[1]/div[2]/h3/span").text
# #                             print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_two_player_name = "N/A"
# #                                 print(f"Passing Yards Team Two Player Name: {passing_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a/div[2]").text
# #                             print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 passing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]/div[2]").text
# #                                 print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 passing_yard_team_two_player_states = "N/A"
# #                                 print(f"Passing Yards Team Two Player States : {passing_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[1]/section/div/a[2]")
# #                             click_passing_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_passing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[1]/section/div/a[2]")
# #                                 click_passing_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)
# #                         try:
# #                             passing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             passing_yard_team_two_player_image = passing_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"Passing Yards Team 2 Player Image: {passing_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Passing Yards Team 2 Player Image not found within the given time.")
# #                             passing_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Rushing Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_one_player_name = "N/A"
# #                                 print(f"rushing Yards Team One Player Name: {rushing_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                             print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]/div[2]").text
# #                                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_one_player_states = "N/A"
# #                                 print(f"rushing Yards Team One Player States : {rushing_yard_team_one_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[1]")
# #                             click_rushing_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_rushing_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[1]")
# #                                 click_rushing_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)
# #                         try:
# #                             rushing_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             rushing_yard_team_one_player_image = rushing_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"rushing Yards Team 1 Player Image: {rushing_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Rushing Yards Team 1 Player Image not found within the given time.")
# #                             rushing_yard_team_one_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Getting second rushing Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                             print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_two_player_name = "N/A"
# #                                 print(f"rushing Yards Team Two Player Name: {rushing_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                             print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 rushing_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]/div[2]").text
# #                                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 rushing_yard_team_two_player_states = "N/A"
# #                                 print(f"rushing Yards Team Two Player States : {rushing_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[2]/section/div/a[2]")
# #                             click_rushing_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_rushing_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[2]/section/div/a[2]")
# #                                 click_rushing_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)

# #                         try:
# #                             rushing_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             rushing_yard_team_two_player_image = rushing_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"rushing Yards Team 2 Player Image: {rushing_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Rushing Yards Team 2 Player Image not found within the given time.")
# #                             rushing_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Receiving Yards
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                             print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[1]/div[2]/h3/span").text
# #                                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_one_player_name = "N/A"
# #                                 print(f"receiving Yards Team One Player Name: {receiving_yard_team_one_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                             print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_one_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]/div[2]").text
# #                                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_one_player_name = "N/A"
# #                                 print(f"receiving Yards Team One Player States : {receiving_yard_team_one_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[1]")
# #                             click_receiving_yard_team_one_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_receiving_yard_team_one_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[1]")
# #                                 click_receiving_yard_team_one_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)

# #                         try:
# #                             receiving_yard_team_one_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             receiving_yard_team_one_player_image = receiving_yard_team_one_player_image_script.get_attribute('src')
# #                             print(f"receiving Yards Team 1 Player Image: {receiving_yard_team_one_player_image}")
# #                         except TimeoutException:
# #                             print("Receiving Yards Team 1 Player Image not found within the given time.")
# #                             receiving_yard_team_one_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Getting second receiving Yards player data
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                             print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[1]/div[2]/h3/span").text
# #                                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_two_player_name = "N/A"
# #                                 print(f"receiving Yards Team Two Player Name: {receiving_yard_team_two_player_name}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                             print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 receiving_yard_team_two_player_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]/div[2]").text
# #                                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 receiving_yard_team_two_player_states = "N/A"
# #                                 print(f"receiving Yards Team Two Player States : {receiving_yard_team_two_player_states}")

# #                         time.sleep(2)
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[2]/section/div/div[2]/div[3]/section/div/a[2]")
# #                             click_receiving_yard_team_two_player_name.click()
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 click_receiving_yard_team_two_player_name = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[3]/section/div/div[2]/div[3]/section/div/a[2]")
# #                                 click_receiving_yard_team_two_player_name.click()
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 pass

# #                         time.sleep(5)
# #                         try:
# #                             receiving_yard_team_two_player_image_script = WebDriverWait(driver, 10).until(
# #                                 EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]/div[1]/figure[2]/div[2]/img"))
# #                             )
# #                             receiving_yard_team_two_player_image = receiving_yard_team_two_player_image_script.get_attribute('src')
# #                             print(f"receiving Yards Team 2 Player Image: {receiving_yard_team_two_player_image}")
# #                         except TimeoutException:
# #                             print("Receiving Yards Team 2 Player Image not found within the given time.")
# #                             receiving_yard_team_two_player_image = "N/A"

# #                         # Go back to the Match page
# #                         driver.back()

# #                         # Team Stats
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[1]/span").text
# #                             print(f"Team One Total Yards States : {team_one_total_yards_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[1]/span").text
# #                                 print(f"Team One Total Yards States : {team_one_total_yards_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_total_yards_states = "N/A"
# #                                 print(f"Team One Total Yards States : {team_one_total_yards_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[2]/div[2]/span").text
# #                             print(f"Team Two Total Yards States : {team_two_total_yards_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_total_yards_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[2]/div[2]/span").text
# #                                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_total_yards_states = "N/A"
# #                                 print(f"Team Two Total Yards States : {team_two_total_yards_states}")

# #                         # Turnovers
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[1]/span").text
# #                             print(f"Team One Turnovers States : {team_one_turnovers_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[1]/span").text
# #                                 print(f"Team One Turnovers States : {team_one_turnovers_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_turnovers_states = "N/A"
# #                                 print(f"Team One Turnovers States : {team_one_turnovers_states}")
                        
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[3]/div[2]/span").text
# #                             print(f"Team Two Total Yards States : {team_two_turnovers_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_turnovers_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[3]/div[2]/span").text
# #                                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_turnovers_states = "N/A"
# #                                 print(f"Team Two Total Yards States : {team_two_turnovers_states}")

# #                         # 1st Downs
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[1]/span").text
# #                             print(f"Team One first_downs States : {team_one_first_downs_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[1]/span").text
# #                                 print(f"Team One first_downs States : {team_one_first_downs_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_first_downs_states = "N/A"
# #                                 print(f"Team One first_downs States : {team_one_first_downs_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[4]/div[2]/span").text
# #                             print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_first_downs_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[4]/div[2]/span").text
# #                                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_first_downs_states = "N/A"
# #                                 print(f"Team Two Total 1st Downs States : {team_two_first_downs_states}")
                        
# #                         # Time of Possession
# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[1]").text
# #                             print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_one_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[1]").text
# #                                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_one_time_of_possession_states = "N/A"
# #                                 print(f"Team One time_of_possession States : {team_one_time_of_possession_states}")

# #                         try:
# #                             # First attempt: Try to find the element using the first XPath
# #                             team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[4]/section/div/div[5]/div/span[2]").text
# #                             print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
# #                         except NoSuchElementException:
# #                             try:
# #                                 # Second attempt: If the first XPath failed, try the second one
# #                                 team_two_time_of_possession_states = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div/div/div[3]/div/div[1]/div[5]/section/div/div[5]/div/span[2]").text
# #                                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
# #                             except NoSuchElementException:
# #                                 # Final fallback: If both XPaths failed, set the variable to "N/A"
# #                                 team_two_time_of_possession_states = "N/A"
# #                                 print(f"Team Two Total Time of Possession States : {team_two_time_of_possession_states}")
                        
        
# #                         live_data = [team_one_name, team_one_records, team_one_live_score, team_two_name, team_two_records, team_two_live_score, team_one_image, 
# #                                     team_two_image, passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
# #                                     passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
# #                                     passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
# #                                     rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
# #                                     rushing_yard_team_two_player_name, rushing_yard_team_two_player_states, 
# #                                     rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states,
# #                                 receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
# #                                     receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
# #                                     team_one_total_yards_states, team_two_total_yards_states, team_one_turnovers_states, team_two_turnovers_states, 
# #                                     team_one_first_downs_states, team_two_first_downs_states, team_one_time_of_possession_states, team_two_time_of_possession_states]

# #                         live_csv_writer.writerow(live_data)
# #                         driver.back()

# #                     else:
# #                         print(f"Game status is {game_status}. Skipping for now.")
# #                         continue

# #                 scraped_weeks.add(week_number)
# #             with open(scraped_weeks_file, 'a') as f:
# #                 f.write(str(week_number) + '\n')

        
# #         next_game_start_date = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[1]/header/div[1]/h3").text

# #         # Parse the original string into a datetime object
# #         date_object = datetime.datetime.strptime(next_game_start_date, "%A, %B %d, %Y")

# #         # Format the datetime object to the desired output
# #         next_game_date = f"{date_object.year},{date_object.month},{date_object.day}"

# #         print(next_game_date)

                
# #     except Exception as e:
# #         print(f"An unexpected error occurred: {e}")
# #         driver.quit()


# #     finally:
# #         final_csv_file.close()
# #         live_csv_file.close()
# #         driver.quit()














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
# from selenium.common.exceptions import TimeoutException

# # --- SETUP ---
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://www.espn.com/nfl/scoreboard/_/week/6/year/2025/seasontype/2")
# time.sleep(5)

# # --- CSV SETUP ---
# final_headers = [
#     "Team_one_logo","team_one_name","team_one_score","team_one_records","team_two_logo","team_two_name","team_two_score","team_two_records",
#     "team_one_passing_yard_player_image","team_one_passing_yard_player_name","team_one_passing_yard_player_position","team_one_passing_yard_player_game_state","team_one_player_one_passing_yard",
#     "team_two_passing_yard_player_image","team_two_passing_yard_player_name","team_two_passing_yard_player_position","team_two_passing_yard_player_game_state","team_two_player_two_passing_yard",
#     "team_one_rushing_yard_player_image","team_one_rushing_yard_player_name","team_one_rushing_yard_player_position","team_one_rushing_yard_player_game_state","team_one_player_one_rushing_yard",
#     "team_two_rushing_yard_player_image","team_two_rushing_yard_player_name","team_two_rushing_yard_player_position","team_two_rushing_yard_player_game_state","team_two_player_two_rushing_yard",
#     "team_one_receiving_yard_player_image","team_one_receiving_yard_player_name","team_one_receiving_yard_player_position","team_one_receiving_yard_player_game_state","team_one_player_one_receiving_yard",
#     "team_two_receiving_yard_player_image","team_two_receiving_yard_player_name","team_two_receiving_yard_player_position","team_two_receiving_yard_player_game_state","team_two_player_two_receiving_yard",
#     "team_one_sacks_player_image","team_one_sacks_player_name","team_one_sacks_player_position","team_one_player_one_sacks","team_two_sacks_player_image","team_two_sacks_player_name","team_two_sacks_player_position","team_two_player_two_sacks",
#     "team_one_tackles_player_image","team_one_tackles_player_name","team_one_tackles_player_position","team_one_tackles_player_game_state","team_one_player_one_tackles","team_two_tackles_player_image","team_two_tackles_player_name","team_two_tackles_player_position","team_two_tackles_player_game_state","team_two_player_two_tackles"
# ]

# # Open the CSV file and write the headers
# final_csv_file = open('final.csv', 'w', newline='', encoding='utf-8')
# final_csv_writer = csv.writer(final_csv_file)
# final_csv_writer.writerow(final_headers)

# live_headers = ["team_1_name", "team_1_records", "team_1_score", "team_2_name", "team_2_records", "team_2_score", "team_1_logo", "team_2_logo", "pass_p1_name", "pass_p1_stats", 
#                 "pass_p1_img", "pass_p2_name", "pass_p2_stats", "pass_p2_img", "rush_p1_name", "rush_p1_stats",
#                 "rush_p1_img", "rush_p2_name", "rush_p2_stats", "rush_p2_img", "rec_p1_name", "rec_p1_stats", "rec_p1_img", "rec_p2_name", 
#                 "rec_p2_stats", "rec_p2_img", "team_1_total_yards", "team_2_total_yards", "team_1_turnovers", "team_2_turnovers", "team_1_first_downs", 
#                 "team_2_first_downs", "team_1_time_possession", "team_2_time_possession"
# ]


# # Open the CSV file and write the headers
# live_csv_file = open('live.csv', 'w', newline='', encoding='utf-8')
# live_csv_writer = csv.writer(live_csv_file)
# live_csv_writer.writerow(live_headers)


# finished_games = []

# try:
#     game_sections = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section")
#     num_days = len(game_sections)
#     print("-----------------------------------------------")
#     print(f"The number of days found is: {num_days}")
#     print("-----------------------------------------------")
#     print("\n")

#     for i in range(num_days):
#         games_in_day = driver.find_elements(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section")
#         number_of_games_in_day = len(games_in_day)
#         game_date = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[{i+1}]/header/div[1]/h3").text
#         print("-----------------------------------------------")
#         print(f"For {game_date}: The number of games is: {number_of_games_in_day}")
#         print("-----------------------------------------------")
#         print("\n")

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

#             # The main check: if the game hasn't been scraped yet
#             if game_id not in finished_games:
#                 if game_status == "FINAL":
#                     try:
#                         print("Scraping a FINAL game.")
#                         click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div[1]/div[1]/div/div/section[{i+1}]/div/section[{j+1}]/div[2]/a[1]")
#                         click_gamecast_button.click()
#                         # Add the game ID to the list to prevent future scraping
#                         finished_games.append(game_id)
#                     except NoSuchElementException:
#                         print("Click Gamecast button not found.")
#                         continue

#                     time.sleep(5)

#                     try:
#                         team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/a/picture/img")
#                         team_one_logo = team_one_logo_element.get_attribute('src') 
#                         print(f"Team 1 logo: {team_one_logo}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/a/picture/img")
#                             team_one_logo = team_one_logo_element.get_attribute('src')
#                             print(f"Team 1 logo: {team_one_logo}")
#                         except NoSuchElementException:
#                             team_one_logo = "N/A"
#                             print(f"Team 1 logo: {team_one_logo}")
                            
#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/div/div/div[1]/div/a/span[1]").text
#                         print(f"Team 1 Name: {team_one_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div/div/div[1]/div/a/span[2]").text
#                             print(f"Team 1 Name: {team_one_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_name = "N/A"
#                             print(f"Team 1 Name: {team_one_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[2]/div[1]").text
#                         print(f"Team 1 Score: {team_one_score}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[2]/div[1]").text
#                             print(f"Team 1 Score: {team_one_score}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_score = "N/A"
#                             print(f"Team 1 Score: {team_one_score}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[1]/div/div/div[2]/span[1]").text
#                         print(f"Team 1 Record: {team_one_records}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[5]/div[1]/div/div/div[2]/span").text
#                             print(f"Team 1 Record: {team_one_records}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_records = "N/A"
#                             print(f"Team 1 Record: {team_one_records}")

#                     try:
#                         team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/a/picture/img")
#                         team_two_logo = team_two_logo_element.get_attribute('src') 
#                         print(f"Team 1 logo: {team_two_logo}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/a/picture/img")
#                             team_two_logo = team_two_logo_element.get_attribute('src')
#                             print(f"Team 1 logo: {team_two_logo}")
#                         except NoSuchElementException:
#                             team_two_logo = "N/A"
#                             print(f"Team 1 logo: {team_two_logo}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
#                         print(f"Team 2 Name: {team_two_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
#                             print(f"Team 2 Name: {team_two_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_name = "N/A"
#                             print(f"Team 2 Name: {team_two_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[2]/div[1]").text
#                         print(f"Team 2 Score: {team_two_score}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[2]/div[1]").text
#                             print(f"Team 2 Score: {team_two_score}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_score = "N/A"
#                             print(f"Team 2 Score: {team_two_score}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[7]/div[1]/div/div/div[2]/span[1]").text
#                         print(f"Team 2 Record: {team_two_records}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[7]/div[1]/div/div/div[2]/span").text
#                             print(f"Team 2 Record: {team_two_records}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_records = "N/A"
#                             print(f"Team 2 Record: {team_two_records}")

#                     print("\n--------------------------------")
#                     print("Game Leaders")
#                     print("--------------------------------\n")

#                     try:
#                         team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
#                         full_image_url = team_one_image_element.get_attribute('src') 
#                         team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")

#                     except NoSuchElementException:
#                         try:
#                             team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[1]/picture/img")
#                             full_image_url = team_one_image_element.get_attribute('src')
#                             team_one_passing_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")
#                         except NoSuchElementException:
#                             team_one_passing_yard_player_image = "N/A"
#                             print(f"Team 2 Passing Yard Player Image: {team_one_passing_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_passing_yard_player_name = "N/A"
#                             print(f"Team 1 Passing Yard player Name: {team_one_passing_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_passing_yard_player_position = "N/A"
#                             print(f"Team 1 Passing Yard player Position: {team_one_passing_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_passing_yard_player_game_state = "N/A"
#                             print(f"Team 1 Passing Yard player game_state: {team_one_passing_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
#                         print(f"Team 1 Player One Passing Yard: {team_one_player_one_passing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_player_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[1]/div/div[2]/div[2]/span").text
#                             print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_player_one_passing_yard = "N/A"
#                             print(f"Team 1 Passing Yard: {team_one_player_one_passing_yard}")

#                     try:
#                         team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
#                         full_image_url = team_two_image_element.get_attribute('src') 
#                         team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[1]/picture/img")
#                             full_image_url = team_two_image_element.get_attribute('src')
#                             team_two_passing_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")
#                         except NoSuchElementException:
#                             team_two_passing_yard_player_image = "N/A"
#                             print(f"Team 2 Passing Yard Player Image: {team_two_passing_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_passing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_passing_yard_player_name = "N/A"
#                             print(f"Team 2 Passing Yard player Name: {team_two_passing_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_passing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_passing_yard_player_position = "N/A"
#                             print(f"Team 2 Passing Yard player Position: {team_two_passing_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_passing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_passing_yard_player_game_state = "N/A"
#                             print(f"Team 2 Passing Yard player game_state: {team_two_passing_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
#                         print(f"Team 2 Player two Passing Yard: {team_two_player_two_passing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_player_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[1]/a[2]/div/div[2]/div[2]/span").text
#                             print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_player_two_passing_yard = "N/A"
#                             print(f"Team 2 Passing Yard: {team_two_player_two_passing_yard}")

                    
#                     print("\n--------------------------------")
#                     print("Rushing Yards")
#                     print("--------------------------------\n")

#                     try:
#                         team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[1]/picture/img")
#                         full_image_url = team_one_image_element.get_attribute('src') 
#                         team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")

#                     except NoSuchElementException:
#                         try:
#                             team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[1]/picture/img")
#                             full_image_url = team_one_image_element.get_attribute('src')
#                             team_one_rushing_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")
#                         except NoSuchElementException:
#                             team_one_rushing_yard_player_image = "N/A"
#                             print(f"Team 2 rushing Yard Player Image: {team_one_rushing_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_rushing_yard_player_name = "N/A"
#                             print(f"Team 1 rushing Yard player Name: {team_one_rushing_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_rushing_yard_player_position = "N/A"
#                             print(f"Team 1 rushing Yard player Position: {team_one_rushing_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_rushing_yard_player_game_state = "N/A"
#                             print(f"Team 1 rushing Yard player game_state: {team_one_rushing_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
#                         print(f"Team 1 Player One rushing Yard: {team_one_player_one_rushing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_player_one_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[1]/div/div[2]/div[2]/span").text
#                             print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_player_one_rushing_yard = "N/A"
#                             print(f"Team 1 rushing Yard: {team_one_player_one_rushing_yard}")

#                     try:
#                         team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
#                         full_image_url = team_two_image_element.get_attribute('src') 
#                         team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_image_element = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[1]/picture/img")
#                             full_image_url = team_two_image_element.get_attribute('src')
#                             team_two_rushing_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")
#                         except NoSuchElementException:
#                             team_two_rushing_yard_player_image = "N/A"
#                             print(f"Team 2 rushing Yard Player Image: {team_two_rushing_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_rushing_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_rushing_yard_player_name = "N/A"
#                             print(f"Team 2 rushing Yard player Name: {team_two_rushing_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_rushing_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_rushing_yard_player_position = "N/A"
#                             print(f"Team 2 rushing Yard player Position: {team_two_rushing_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_rushing_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_rushing_yard_player_game_state = "N/A"
#                             print(f"Team 2 rushing Yard player game_state: {team_two_rushing_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
#                         print(f"Team 2 Player two rushing Yard: {team_two_player_two_rushing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_player_two_rushing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[2]/a[2]/div/div[2]/div[2]/span").text
#                             print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_player_two_rushing_yard = "N/A"
#                             print(f"Team 2 rushing Yard: {team_two_player_two_rushing_yard}")

#                     print("\n--------------------------------")
#                     print("Receiving Yards")
#                     print("--------------------------------\n")

#                     try:
#                         team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
#                         full_image_url = team_one_image_element.get_attribute('src') 
#                         team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[1]/picture/img")
#                             full_image_url = team_one_image_element.get_attribute('src')
#                             team_one_receiving_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")
#                         except NoSuchElementException:
#                             team_one_receiving_yard_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_one_receiving_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_receiving_yard_player_name = "N/A"
#                             print(f"Team 1 receiving Yard player Name: {team_one_receiving_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_receiving_yard_player_position = "N/A"
#                             print(f"Team 1 receiving Yard player Position: {team_one_receiving_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_receiving_yard_player_game_state = "N/A"
#                             print(f"Team 1 receiving Yard player game_state: {team_one_receiving_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
#                         print(f"Team 1 Player One receiving Yard: {team_one_player_one_receiving_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_player_one_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[1]/div/div[2]/div[2]/span").text
#                             print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_player_one_receiving_yard = "N/A"
#                             print(f"Team 1 receiving Yard: {team_one_player_one_receiving_yard}")

#                     try:
#                         team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
#                         full_image_url = team_two_image_element.get_attribute('src') 
#                         team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[1]/picture/img")
#                             full_image_url = team_two_image_element.get_attribute('src')
#                             team_two_receiving_yard_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")
#                         except NoSuchElementException:
#                             team_two_receiving_yard_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_two_receiving_yard_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_receiving_yard_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_receiving_yard_player_name = "N/A"
#                             print(f"Team 2 receiving Yard player Name: {team_two_receiving_yard_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_receiving_yard_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_receiving_yard_player_position = "N/A"
#                             print(f"Team 2 receiving Yard player Position: {team_two_receiving_yard_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_receiving_yard_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_receiving_yard_player_game_state = "N/A"
#                             print(f"Team 2 receiving Yard player game_state: {team_two_receiving_yard_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
#                         print(f"Team 2 Player two receiving Yard: {team_two_player_two_receiving_yard}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_player_two_receiving_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[3]/a[2]/div/div[2]/div[2]/span").text
#                             print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_player_two_receiving_yard = "N/A"
#                             print(f"Team 2 receiving Yard: {team_two_player_two_receiving_yard}")

#                     print("\n--------------------------------")
#                     print("Sacks")
#                     print("--------------------------------\n")

#                     try:
#                         team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[1]/picture/img")
#                         full_image_url = team_one_image_element.get_attribute('src') 
#                         team_one_sacks_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[1]/picture/img")
#                             full_image_url = team_one_image_element.get_attribute('src')
#                             team_one_sacks_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")
#                         except NoSuchElementException:
#                             team_one_sacks_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_one_sacks_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[1]").text
#                         print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[1]").text
#                             print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_sacks_player_name = "N/A"
#                             print(f"Team 1 receiving Yard player Name: {team_one_sacks_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[2]").text
#                         print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[1]/div/span[2]").text
#                             print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_sacks_player_position = "N/A"
#                             print(f"Team 1 receiving Yard player Position: {team_one_sacks_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[2]/span").text
#                         print(f"Team 1 Player One receiving Yard: {team_one_player_one_sacks}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_player_one_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[1]/div/div[2]/div[2]/span").text
#                             print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_player_one_sacks = "N/A"
#                             print(f"Team 1 receiving Yard: {team_one_player_one_sacks}")

#                     try:
#                         team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[1]/picture/img")
#                         full_image_url = team_two_image_element.get_attribute('src') 
#                         team_two_sacks_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[1]/picture/img")
#                             full_image_url = team_two_image_element.get_attribute('src')
#                             team_two_sacks_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")
#                         except NoSuchElementException:
#                             team_two_sacks_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_two_sacks_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
#                         print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_sacks_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[1]").text
#                             print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_sacks_player_name = "N/A"
#                             print(f"Team 2 receiving Yard player Name: {team_two_sacks_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
#                         print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_sacks_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[1]/div/span[2]").text
#                             print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_sacks_player_position = "N/A"
#                             print(f"Team 2 receiving Yard player Position: {team_two_sacks_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
#                         print(f"Team 2 Player two receiving Yard: {team_two_player_two_sacks}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_player_two_sacks = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[4]/a[2]/div/div[2]/div[2]/span").text
#                             print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_player_two_sacks = "N/A"
#                             print(f"Team 2 receiving Yard: {team_two_player_two_sacks}")

#                     print("\n--------------------------------")
#                     print("Tackles")
#                     print("--------------------------------\n")

#                     try:
#                         team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
#                         full_image_url = team_one_image_element.get_attribute('src') 
#                         team_one_tackles_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")

#                     except NoSuchElementException:
#                         try:
#                             team_one_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[1]/picture/img")
#                             full_image_url = team_one_image_element.get_attribute('src')
#                             team_one_tackles_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")
#                         except NoSuchElementException:
#                             team_one_tackles_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_one_tackles_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_tackles_player_name = "N/A"
#                             print(f"Team 1 receiving Yard player Name: {team_one_tackles_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_tackles_player_position = "N/A"
#                             print(f"Team 1 receiving Yard player Position: {team_one_tackles_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_tackles_player_game_state = driver.find_element(By.XPATH, "//html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_tackles_player_game_state = "N/A"
#                             print(f"Team 1 receiving Yard player game_state: {team_one_tackles_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
#                         print(f"Team 1 Player One receiving Yard: {team_one_player_one_tackles}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_one_player_one_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[1]/div/div[2]/div[2]/span").text
#                             print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_player_one_tackles = "N/A"
#                             print(f"Team 1 receiving Yard: {team_one_player_one_tackles}")

#                     try:
#                         team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[1]/picture/img")
#                         full_image_url = team_two_image_element.get_attribute('src') 
#                         team_two_tackles_player_image = full_image_url.split('&', 1)[0]
#                         print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_image_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[1]/picture/img")
#                             full_image_url = team_two_image_element.get_attribute('src')
#                             team_two_tackles_player_image = full_image_url.split('&', 1)[0]
#                             print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")
#                         except NoSuchElementException:
#                             team_two_tackles_player_image = "N/A"
#                             print(f"Team 2 receiving Yard Player Image: {team_two_tackles_player_image}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_tackles_player_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_tackles_player_name = "N/A"
#                             print(f"Team 2 receiving Yard player Name: {team_two_tackles_player_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_tackles_player_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_tackles_player_position = "N/A"
#                             print(f"Team 2 receiving Yard player Position: {team_two_tackles_player_position}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
#                         print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_tackles_player_game_state = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[1]/div[2]").text
#                             print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_tackles_player_game_state = "N/A"
#                             print(f"Team 2 receiving Yard player game_state: {team_two_tackles_player_game_state}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
#                         print(f"Team 2 Player two receiving Yard: {team_two_player_two_tackles}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_player_two_tackles = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[3]/div/div[2]/section[5]/a[2]/div/div[2]/div[2]/span").text
#                             print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_player_two_tackles = "N/A"
#                             print(f"Team 2 receiving Yard: {team_two_player_two_tackles}")
                    
#                     final_data = [team_one_logo,team_one_name,team_one_score,team_one_records,team_two_logo,team_two_name,team_two_score,team_two_records,
#                                 team_one_passing_yard_player_image,team_one_passing_yard_player_name,team_one_passing_yard_player_position,team_one_passing_yard_player_game_state,team_one_player_one_passing_yard,
#                                 team_two_passing_yard_player_image,team_two_passing_yard_player_name,team_two_passing_yard_player_position,team_two_passing_yard_player_game_state,team_two_player_two_passing_yard,
#                                 team_one_rushing_yard_player_image,team_one_rushing_yard_player_name,team_one_rushing_yard_player_position,team_one_rushing_yard_player_game_state,team_one_player_one_rushing_yard,
#                                 team_two_rushing_yard_player_image,team_two_rushing_yard_player_name,team_two_rushing_yard_player_position,team_two_rushing_yard_player_game_state,team_two_player_two_rushing_yard,
#                                 team_one_receiving_yard_player_image,team_one_receiving_yard_player_name,team_one_receiving_yard_player_position,team_one_receiving_yard_player_game_state,team_one_player_one_receiving_yard,
#                                 team_two_receiving_yard_player_image,team_two_receiving_yard_player_name,team_two_receiving_yard_player_position,team_two_receiving_yard_player_game_state,team_two_player_two_receiving_yard,
#                                 team_one_sacks_player_image,team_one_sacks_player_name,team_one_sacks_player_position,team_one_player_one_sacks,team_two_sacks_player_image,team_two_sacks_player_name,team_two_sacks_player_position,team_two_player_two_sacks,
#                                 team_one_tackles_player_image,team_one_tackles_player_name,team_one_tackles_player_position,team_one_tackles_player_game_state,team_one_player_one_tackles,team_two_tackles_player_image,team_two_tackles_player_name,team_two_tackles_player_position,team_two_tackles_player_game_state,team_two_player_two_tackles]
                    
#                     final_csv_writer.writerow(final_data)
                    
#                     driver.back()

#                 elif any(quarter in game_status for quarter in ["1st", "2nd", "3rd", "4th", "Halftime"]):
#                     # --- SCRAPING AND PRINTING ALL LIVE DATA ---
#                     print("----------------------------------------")
#                     print(f"Game is still in progress: {game_status}")

#                     try:
#                         print("Scraping a LIVE game.")
#                         click_gamecast_button = driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/div/main/div[2]/div[2]/div/div/div[1]/div/div/section[1]/div/section[{j+1}]/div[2]/a[1]")
#                         click_gamecast_button.click()
#                         # Add the game ID to the list to prevent future scraping
#                         finished_games.append(game_id)
#                     except NoSuchElementException:
#                         print("Click Gamecast button not found.")
#                         continue

#                     time.sleep(5)

#                     try:
#                         team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/a/picture/img")
#                         team_one_logo = team_one_logo_element.get_attribute('src') 
#                         print(f"Team 1 logo: {team_one_logo}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/a/picture/img")
#                             team_one_logo = team_one_logo_element.get_attribute('src')
#                             print(f"Team 1 logo: {team_one_logo}")
#                         except NoSuchElementException:
#                             team_one_logo = "N/A"
#                             print(f"Team 1 logo: {team_one_logo}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[1]/div/a/span[1]").text
#                         print(f"Team 1 Name: {team_one_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[1]/div/a/span[2]").text
#                             print(f"Team 1 Name: {team_one_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_name = "N/A"
#                             print(f"Team 1 Name: {team_one_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div[5]/div[2]/div[1]").text
#                         print(f"Team 1 Score: {team_one_score}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[2]/div[1]").text
#                             print(f"Team 1 Score: {team_one_score}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_score = "N/A"
#                             print(f"Team 1 Score: {team_one_score}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[2]/span[1]").text
#                         print(f"Team 1 Record: {team_one_records}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_one_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[5]/div[1]/div/div/div[2]/span[1]").text
#                             print(f"Team 1 Record: {team_one_records}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_one_records = "N/A"
#                             print(f"Team 1 Record: {team_one_records}")

#                     try:
#                         team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/a/picture/img")
#                         team_one_logo = team_one_logo_element.get_attribute('src') 
#                         print(f"Team 1 logo: {team_one_logo}")

#                     except NoSuchElementException:
#                         try:
#                             team_one_logo_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/a/picture/img")
#                             team_one_logo = team_one_logo_element.get_attribute('src')
#                             print(f"Team 1 logo: {team_one_logo}")
#                         except NoSuchElementException:
#                             team_one_logo = "N/A"
#                             print(f"Team 1 logo: {team_one_logo}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
#                         print(f"Team 2 Name: {team_two_name}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second one
#                             team_two_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[1]/div/a/span[1]").text
#                             print(f"Team 2 Name: {team_two_name}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_name = "N/A"
#                             print(f"Team 2 Name: {team_two_name}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[2]/div[1]").text
#                         print(f"Team 2 Score: {team_two_score}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_score = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[2]/div[1]").text
#                             print(f"Team 2 Score: {team_two_score}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_score = "N/A"
#                             print(f"Team 2 Score: {team_two_score}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[2]/span[1]").text
#                         print(f"Team 2 Record: {team_two_records}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             team_two_records = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[7]/div[1]/div/div/div[2]/span[1]").text
#                             print(f"Team 2 Record: {team_two_records}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             team_two_records = "N/A"
#                             print(f"Team 2 Record: {team_two_records}")

#                     try:
#                         # First attempt: Try to find the element using the first XPath
#                         yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div[2]/div[1]/span[2]").text
#                         print(f"Yards: {yards}")
#                     except NoSuchElementException:
#                         try:
#                             # Second attempt: If the first XPath failed, try the second two
#                             yards = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[1]/div[3]").text
#                             print(f"Yards: {yards}")
#                         except NoSuchElementException:
#                             # Final fallback: If both XPaths failed, set the variable to "N/A"
#                             yards = "N/A"
#                             print(f"Yards: {yards}")

#                     try:
#                         raw_text = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[1]/div/div[1]/div[2]/div[2]/div").text
#                         ball_on = raw_text.replace('\n', ' ').strip()
                        
#                         print(f"Ball On: {ball_on}")

#                     except NoSuchElementException:
#                         try:
#                             raw_text = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[1]/div[3]").text
#                             ball_on = raw_text.replace('\n', ' ').strip()
#                             print(f"Ball On: {ball_on}")
                            
#                         except NoSuchElementException:
#                             # Final fallback
#                             print(f"Ball On: {ball_on}")

#                     try:
#                         place_to_watch = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[2]/button/p").text
#                         print(f"Place to Watch: {place_to_watch}")
#                     except NoSuchElementException:
#                         try:
#                             place_to_watch = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/div[6]/div[2]/button/p").text
#                             print(f"Place to Watch: {place_to_watch}")
#                         except NoSuchElementException:
#                             place_to_watch = "N/A";
#                             print(f"Place to Watch: {place_to_watch}")

#                     print("\n")
#                     print("----------------------------------------")
#                     print("Game Leaders")
#                     print("----------------------------------------")
#                     print("\n")

#                     try:
#                         team_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Place to Passing Yard Leader: {team_one_passing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Place to Passing Yard Leader: {team_one_passing_yard}")
#                         except NoSuchElementException:
#                             team_one_passing_yard = "N/A";
#                             print(f"Place to Passing Yard Leader: {team_one_passing_yard}")

#                     try:
#                         team_one_passing_yard_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Place to Passing Yard Leader Position: {team_one_passing_yard_position}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_passing_yard_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Place to Passing Yard Leader Position: {team_one_passing_yard_position}")
#                         except NoSuchElementException:
#                             team_one_passing_yard_position = "N/A";
#                             print(f"Place to Passing Yard Leader Position: {team_one_passing_yard_position}")

#                     try:
#                         team_one_passing_yard_states = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Place to Passing Yard Leader states: {team_one_passing_yard_states}")
#                     except NoSuchElementException:
#                         try:
#                             team_one_passing_yard_states = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Place to Passing Yard Leader states: {team_one_passing_yard_states}")
#                         except NoSuchElementException:
#                             team_one_passing_yard_states = "N/A";
#                             print(f"Place to Passing Yard Leader states: {team_one_passing_yard_states}")

#                     try:
#                         team_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                         print(f"Place to Passing Yard Leader: {team_two_passing_yard}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_passing_yard = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[1]").text
#                             print(f"Place to Passing Yard Leader: {team_two_passing_yard}")
#                         except NoSuchElementException:
#                             team_two_passing_yard = "N/A";
#                             print(f"Place to Passing Yard Leader: {team_two_passing_yard}")

#                     try:
#                         team_two_passing_yard_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                         print(f"Place to Passing Yard Leader Position: {team_two_passing_yard_position}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_passing_yard_position = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[1]/span[2]").text
#                             print(f"Place to Passing Yard Leader Position: {team_two_passing_yard_position}")
#                         except NoSuchElementException:
#                             team_two_passing_yard_position = "N/A";
#                             print(f"Place to Passing Yard Leader Position: {team_two_passing_yard_position}")

#                     try:
#                         team_two_passing_yard_states = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                         print(f"Place to Passing Yard Leader states: {team_two_passing_yard_states}")
#                     except NoSuchElementException:
#                         try:
#                             team_two_passing_yard_states = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[2]/div/div[2]/div/div[2]/div[2]/div/div/section[4]/div/div[2]/section[1]/a[1]/div/div[2]/div[1]/div[2]").text
#                             print(f"Place to Passing Yard Leader states: {team_two_passing_yard_states}")
#                         except NoSuchElementException:
#                             team_two_passing_yard_states = "N/A";
#                             print(f"Place to Passing Yard Leader states: {team_two_passing_yard_states}")
    
#                     live_data = [team_one_name, team_one_records, team_one_live_score, team_two_name, team_two_records, team_two_live_score, team_one_image, 
#                                  team_two_image, passing_yard_team_one_player_name, passing_yard_team_one_player_states, 
#                                  passing_yard_team_one_player_image, passing_yard_team_two_player_name, passing_yard_team_two_player_states, 
#                                 passing_yard_team_two_player_image, rushing_yard_team_one_player_name, 
#                                  rushing_yard_team_one_player_states, rushing_yard_team_one_player_image, 
#                                  rushing_yard_team_two_player_name, rushing_yard_team_two_player_states, 
#                                  rushing_yard_team_two_player_image, receiving_yard_team_one_player_name, receiving_yard_team_one_player_states,
#                                receiving_yard_team_one_player_image, receiving_yard_team_two_player_name, 
#                                  receiving_yard_team_two_player_states, receiving_yard_team_two_player_image, 
#                                  team_one_total_yards_states, team_two_total_yards_states, team_one_turnovers_states, team_two_turnovers_states, 
#                                  team_one_first_downs_states, team_two_first_downs_states, team_one_time_of_possession_states, team_two_time_of_possession_states]

#                     live_csv_writer.writerow(live_data)
#                     driver.back()

#                 else:
#                     print("--------------------------------------------------")
#                     print(f"Game status is {game_status}. Skipping for now.")
#                     print("--------------------------------------------------")
#                     print("\n")
#                     continue
#             else:
#                 print(f"Game with ID {game_id} already scraped. Skipping.")
            
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
#     driver.quit()

# finally:
#     final_csv_file.close()
#     live_csv_file.close()
#     driver.quit()










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
from database_helpers import (
    get_team_id_by_name, 
    insert_or_update_game, 
    insert_or_update_player, 
    insert_game_stats, 
    insert_player_game_stats,
    log_scraping_attempt,
    safe_int_conversion
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

# --- DATABASE PROCESSING FUNCTIONS ---
def extract_game_id_from_url(url):
    """Extract game ID from ESPN URL"""
    # ESPN URLs typically have format like: /nfl/game/_/gameId/401547123
    match = re.search(r'/gameId/(\d+)', url)
    return match.group(1) if match else None

def parse_game_state(game_state_str):
    """Parse game state string to extract numeric values"""
    if not game_state_str or game_state_str == "N/A":
        return None
    
    # Extract numbers from strings like "6/12, 1 INT" or "10 CAR, 1 TD"
    numbers = re.findall(r'\d+', game_state_str)
    return int(numbers[0]) if numbers else None

def process_player_data(player_name, player_position, player_image, team_id, stat_type, stat_value, game_state):
    """Process player data for database insertion"""
    if not player_name or player_name == "N/A":
        return None
    
    # Insert or get player
    player_data = {
        "player_name": player_name,
        "position": player_position,
        "team_id": team_id,
        "player_image_url": player_image if player_image != "N/A" else None
    }
    
    player_id = insert_or_update_player(player_data)
    
    if player_id:
        return {
            "player_id": player_id,
            "team_id": team_id,
            "stat_type": stat_type,
            "stat_value": parse_game_state(stat_value),
            "game_state": game_state
        }
    return None

def process_team_stats(game_id, team_id, score, total_yards, total_turnovers, first_downs, 
                      penalties, third_down, fourth_down, red_zone, possession):
    """Process team statistics for database insertion"""
    return {
        "game_id": game_id,
        "team_id": team_id,
        "score": safe_int_conversion(score),
        "total_yards": safe_int_conversion(total_yards),
        "total_turnovers": safe_int_conversion(total_turnovers),
        "first_downs": safe_int_conversion(first_downs),
        "penalties": penalties if penalties != "N/A" else "",
        "third_down_conversions": third_down if third_down != "N/A" else "",
        "fourth_down_conversions": fourth_down if fourth_down != "N/A" else "",
        "red_zone_efficiency": red_zone if red_zone != "N/A" else "",
        "time_of_possession": possession if possession != "N/A" else ""
    }

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
                        # Get current URL to extract game ID
                        current_url = driver.current_url
                        game_id = extract_game_id_from_url(current_url)
                        
                        if not game_id:
                            print("Could not extract game ID from URL")
                            log_scraping_attempt("unknown", "failed", "Could not extract game ID")
                        else:
                            # Get team IDs
                            home_team_id = get_team_id_by_name(team_one_name)
                            away_team_id = get_team_id_by_name(team_two_name)
                            
                            if not home_team_id or not away_team_id:
                                print(f"Could not find team IDs for {team_one_name} or {team_two_name}")
                                log_scraping_attempt(game_id, "failed", "Team not found in database")
                            else:
                                # Prepare game data
                                game_data = {
                                    "game_id": game_id,
                                    "home_team_id": home_team_id,
                                    "away_team_id": away_team_id,
                                    "game_status": game_status,
                                    "quarter": game_status,
                                    "time_remaining": None
                                }
                                
                                # Insert/update game
                                if insert_or_update_game(game_data):
                                    # Process team 1 stats
                                    team1_stats = process_team_stats(
                                        game_id, home_team_id, team_one_score, team_one_total_yards, 
                                        team_one_total_turnovers, team_one_first_downs, team_one_penalties, 
                                        team_one_third_down, team_one_forth_down, team_one_red_zone, team_one_possession
                                    )
                                    
                                    # Process team 2 stats
                                    team2_stats = process_team_stats(
                                        game_id, away_team_id, team_two_score, team_two_total_yards, 
                                        team_two_total_turnovers, team_two_first_downs, team_two_penalties, 
                                        team_two_third_down, team_two_forth_down, team_two_red_zone, team_two_possession
                                    )
                                    
                                    # Insert team stats
                                    insert_game_stats(team1_stats)
                                    insert_game_stats(team2_stats)
                                    
                                    # Process player stats for team 1
                                    player_stats_list = []
                                    
                                    # Team 1 Passing stats
                                    if team_one_passing_yard_player_name and team_one_passing_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_one_passing_yard_player_name, 
                                            team_one_passing_yard_player_position,
                                            team_one_passing_yard_player_image,
                                            home_team_id,
                                            "passing",
                                            team_one_player_one_passing_yard,
                                            team_one_passing_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 1 Rushing stats
                                    if team_one_rushing_yard_player_name and team_one_rushing_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_one_rushing_yard_player_name,
                                            team_one_rushing_yard_player_position,
                                            team_one_rushing_yard_player_image,
                                            home_team_id,
                                            "rushing",
                                            team_one_player_one_rushing_yard,
                                            team_one_rushing_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 1 Receiving stats
                                    if team_one_receiving_yard_player_name and team_one_receiving_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_one_receiving_yard_player_name,
                                            team_one_receiving_yard_player_position,
                                            team_one_receiving_yard_player_image,
                                            home_team_id,
                                            "receiving",
                                            team_one_player_one_receiving_yard,
                                            team_one_receiving_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 1 Sacks stats
                                    if team_one_sacks_player_name and team_one_sacks_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_one_sacks_player_name,
                                            team_one_sacks_player_position,
                                            team_one_sacks_player_image,
                                            home_team_id,
                                            "sacks",
                                            team_one_player_one_sacks,
                                            None
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 1 Tackles stats
                                    if team_one_tackles_player_name and team_one_tackles_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_one_tackles_player_name,
                                            team_one_tackles_player_position,
                                            team_one_tackles_player_image,
                                            home_team_id,
                                            "tackles",
                                            team_one_player_one_tackles,
                                            team_one_tackles_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 2 Passing stats
                                    if team_two_passing_yard_player_name and team_two_passing_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_two_passing_yard_player_name, 
                                            team_two_passing_yard_player_position,
                                            team_two_passing_yard_player_image,
                                            away_team_id,
                                            "passing",
                                            team_two_player_two_passing_yard,
                                            team_two_passing_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 2 Rushing stats
                                    if team_two_rushing_yard_player_name and team_two_rushing_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_two_rushing_yard_player_name,
                                            team_two_rushing_yard_player_position,
                                            team_two_rushing_yard_player_image,
                                            away_team_id,
                                            "rushing",
                                            team_two_player_two_rushing_yard,
                                            team_two_rushing_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 2 Receiving stats
                                    if team_two_receiving_yard_player_name and team_two_receiving_yard_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_two_receiving_yard_player_name,
                                            team_two_receiving_yard_player_position,
                                            team_two_receiving_yard_player_image,
                                            away_team_id,
                                            "receiving",
                                            team_two_player_two_receiving_yard,
                                            team_two_receiving_yard_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 2 Sacks stats
                                    if team_two_sacks_player_name and team_two_sacks_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_two_sacks_player_name,
                                            team_two_sacks_player_position,
                                            team_two_sacks_player_image,
                                            away_team_id,
                                            "sacks",
                                            team_two_player_two_sacks,
                                            None
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Team 2 Tackles stats
                                    if team_two_tackles_player_name and team_two_tackles_player_name != "N/A":
                                        player_stat = process_player_data(
                                            team_two_tackles_player_name,
                                            team_two_tackles_player_position,
                                            team_two_tackles_player_image,
                                            away_team_id,
                                            "tackles",
                                            team_two_player_two_tackles,
                                            team_two_tackles_player_game_state
                                        )
                                        if player_stat:
                                            player_stat["game_id"] = game_id
                                            player_stats_list.append(player_stat)
                                    
                                    # Insert all player stats
                                    for player_stat in player_stats_list:
                                        insert_player_game_stats(player_stat)
                                    
                                    # Log successful scraping
                                    log_scraping_attempt(game_id, "success")
                                    print(f"✓ Successfully processed FINAL game: {game_id}")
                                    
                                else:
                                    log_scraping_attempt(game_id, "failed", "Could not insert game data")
                    
                    except Exception as e:
                        print(f"Error processing FINAL game: {e}")
                        log_scraping_attempt(game_id if 'game_id' in locals() else "unknown", "failed", str(e))
                    
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
