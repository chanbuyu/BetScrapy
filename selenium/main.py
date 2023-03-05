from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()

driver.get("https://xbbsportpro.net/A13371#/sports/2/live")

wait = WebDriverWait(driver, 15)
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mainPeriods oddsTable display-length-2')))
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="eventWrap"]/div[@class="mainEventItem isLive main"]')))
print('开始睡眠')
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="mainEventItem isLive main"]/div[@class="mainPeriods oddsTable display-length-2"]')))

time.sleep(1)
#webPage = driver.find_element(By.ID, 'newBBHome')
LeagueItems = driver.find_elements(By.CLASS_NAME, 'leagueItem')
for league_item in LeagueItems:
    try:
        games = league_item.find_elements(By.CLASS_NAME, 'eventWrap')
        for game in games:
            try:
                teamNames = game.find_elements(By.CLASS_NAME, 'teamName')
                for teamName in teamNames:
                    print(teamName.text)
                #mainOdds = game.find_element(By.CLASS_NAME, 'mainPeriods oddsTable display-length-2')
                #print(game.find_element(By.XPATH, '//div[@class="mainEventItem isLive main"]/div[@class="mainPeriods oddsTable display-length-2"]'))
                print(game.find_element(By.XPATH,
                                        '//div[@class="mainPeriods oddsTable display-length-2"]/div[@class="oddsColumn play-OU play-line3"]').text)
            except:
                print('、、、、、、、')

    except:
        print('----------------------------')

driver.quit()