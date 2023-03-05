import scrapy
from selenium import webdriver
from ScrapySelenium.items import ScrapyseleniumItem
from datetime import datetime
import time

def remove_newlines(text):
    return text.replace('\n', '').replace(' ', '')

class Bet365Spider(scrapy.Spider):
    name = "bet365"
    #allowed_domains = ["bet365.com"]
    start_urls = ["https://xbbsportpro.net/A13371#/sports/2/live"]

    def __init__(self):
        super(Bet365Spider, self).__init__()
        #options = webdriver.Firefox()
        #options.add_argument('headless')
        #options.add_argument('--disable-gpu')
        #options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Firefox()

    def close(self, spider):
        self.driver.quit()
        #print('closed spider')

    def parse(self, response):
        #print(response.text)
        i = 0
        while i <= 10 :
            i += 1
            LeagueItems = response.css('.leagueItem')
            print(len(LeagueItems))
            if len(LeagueItems) == 0 :
                print('无数据，开始重新刷新网站！')
                self.driver.refresh()
                time.sleep(10)
            for league_item in LeagueItems:
                try:
                    # 获取联赛名称
                    league_name = league_item.css(".leagueName").css("div::text").get()
                    # 获取同一联赛下多场比赛
                    games = league_item.css('.eventWrap')
                    for game in games:
                        try:
                            # 获取大小盘源代码
                            oddsColumn = game.css("div.oddsColumn.play-OU")
                            outerOddsItems = oddsColumn.css("div.outerOddsItem.isLive")
                            # 让球数量
                            odds_text_wrap = outerOddsItems[0].css(".cap").css("div::text").get()
                            # print("odds-text-wrap:", odds_text_wrap)
                            # 让球盘口
                            bigOdds = outerOddsItems[0].css(".odds.hasOdds").css("div::text").get()
                            smallOdds = outerOddsItems[1].css(".odds.hasOdds").css("div::text").get()

                            teamNames = game.css(".teamName")

                            yield {
                                'time' : datetime.now(),
                                'league' : league_name,
                                'host' : remove_newlines(teamNames[0].css("span::text").get()),
                                'guest' : remove_newlines(teamNames[1].css("span::text").get()),
                                'bigSmall' : float(odds_text_wrap),
                                'bigOdds' : float(remove_newlines(bigOdds)),
                                'smallOdds' : float(remove_newlines(smallOdds))

                            }

                        except:
                            print('该赛事暂无盘口：', remove_newlines(teamNames[0].css("span::text").get()))
                except:
                    print('获取联赛名称失败。。。')

            time.sleep(3)