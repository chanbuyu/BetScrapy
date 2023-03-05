import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from ScrapySelenium.items import ScrapyseleniumItem
from datetime import datetime
import time
from selenium.webdriver.common.by import By

def remove_newlines(text):
    return text.replace('\n', '').replace(' ', '')

class Bet365Spider(scrapy.Spider):
    name = "bet365"
    #allowed_domains = ["bet365.com"]
    start_urls = ["https://sb.eg2jdicjw1kzcxw.com/NewIndex?lang=cs&webskintype=3"]

    def __init__(self):
        super(Bet365Spider, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        # options.add_argument('--disable-gpu')
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_options=options)

    def close(self, spider):
        self.driver.quit()
        #print('closed spider')

    def parse(self, response):
        i = 1
        num = 50000
        while i <= num:
            response = Selector(text=self.driver.page_source)
            print("抓取数据中，还剩下如下次数：", num - i)
            if i % 10 == 0:
                # 选择篮球赛事
                self.driver.find_elements(By.CLASS_NAME, 'c-side-nav__item')[0].click()
                print("已刷新篮球数据")
            time.sleep(5)
            i += 1
            # 今日滚球部分
            TodayGames = response.css('.c-odds-table.c-odds-table--sport2.c-odds-table--in-play')
            # print(len(TodayGames))
            # print(TodayGames.extract())
            LeagueItems = TodayGames.css('.c-league')
            print(len(LeagueItems))
            # if len(LeagueItems) == 0 :
            #     print('无数据，开始重新刷新网站！')
            #     self.driver.refresh()
            #     time.sleep(10)
            for league_item in LeagueItems:
                try:
                    # 获取联赛名称
                    league_name = league_item.css(".c-league__name").css("div::text").get()
                    print(league_name)
                    # 获取同一联赛下多场比赛
                    games = league_item.css('.c-match.c-in-play ')
                    print(len(games))
                    for game in games:
                        try:
                            # 获取比分
                            score = game.css(".c-match-score")
                            #print(score.extract())
                            score_text = score.css(".c-text")
                            print("主队得分：", score_text[0].css("span::text").get())
                            print("客队得分：", score_text[2].css("span::text").get())

                            # 获取比赛时间，只需要分钟
                            game_time = game.css(".c-match-time__minute")
                            print("赛事时间：", game_time.css("::text").get())

                            # 获取多个盘口
                            oddsItems = game.css("div.c-match__odds")
                            print("盘口数量：", len(oddsItems))
                            # 球队名称
                            teamNames = oddsItems[0].css(".c-team-name")
                            print("主队名称：", teamNames[0].css("span::text").get())
                            print("客队名称：", teamNames[1].css("span::text").get())
                            # 只选第一个盘口
                            # 获取大小盘盘口
                            BigSmallColumn = oddsItems[0].css("div.c-bettype-col.c-has-goal")
                            # print(len(BigSmallColumn.extract()))
                            outerOddsItems = BigSmallColumn[1].css("div.c-odds-button")
                            # print(outerOddsItems.extract())

                            # 让球数量
                            odds_text_wrap = outerOddsItems[0].css(".c-text-goal").css("span::text").get()
                            print("odds-text-wrap:", odds_text_wrap)
                            # 让球盘口
                            bigOdds = outerOddsItems[0].css(".c-odds").css("span::text").get()
                            smallOdds = outerOddsItems[1].css(".c-odds").css("span::text").get()
                            print("大：", bigOdds)
                            print("小：", smallOdds)
        #
                            yield {
                                'time': datetime.now(),
                                'league': league_name,
                                'host': remove_newlines(teamNames[0].css("span::text").get()),
                                'guest': remove_newlines(teamNames[1].css("span::text").get()),
                                'gameTime': game_time.css("::text").get(),
                                'hostScore': float(score_text[0].css("span::text").get()),
                                'guestScore': float(score_text[2].css("span::text").get()),
                                'bigSmall': float(odds_text_wrap),
                                'bigOdds': float(remove_newlines(bigOdds)),
                                'smallOdds': float(remove_newlines(smallOdds))
                            }
            #
                        except:
                            print('该赛事暂无盘口：', remove_newlines(teamNames[0].css("span::text").get()))
                except:
                    print('获取联赛名称失败。。。')
            #
            # time.sleep(3)