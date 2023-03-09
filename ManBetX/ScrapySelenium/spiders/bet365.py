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
    start_urls = ["https://cn.mebetx63.com/sports/btisport"]

    def __init__(self):
        super(Bet365Spider, self).__init__()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        #options.add_argument('--disable-gpu')
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver = webdriver.Firefox()

    def close(self, spider):
        self.driver.quit()
        #print('closed spider')

    def parse(self, response):
        # 切换iframe
        # response.switch_to.frame("sb_frame")
        # print("切换到iframe中的源代码")
        #print(response.text)
        i = 1
        num = 50000
        while i <= num :
            response = Selector(text=self.driver.page_source)
            print("抓取数据中，还剩下如下次数：", num - i)
            if i % 2 == 0:
                # 选择篮球赛事
                selenium_TodayGames = self.driver.find_element(By.CLASS_NAME, 'eventlist_asia_fe_EventListSection_container')
                selenium_LeagueItems = selenium_TodayGames.find_elements(By.CLASS_NAME, 'eventlist_asia_fe_EventListLeague_container')
                for league in selenium_LeagueItems:
                    selenium_games = league.find_elements(By.CLASS_NAME, 'eventlist_asia_fe_EventListLeague_singleEvent')
                    #print("selenium_games:", len(selenium_games))
                    if len(selenium_games) == 0:
                        league.find_element(By.CLASS_NAME, 'eventlist_asia_fe_EventListLeague_expandCollapse').click()
                        time.sleep(1)
                print("已刷新篮球数据")
            time.sleep(5)
            i += 1
            # 今日滚球部分
            TodayGames = response.css('.eventlist_asia_fe_EventListSection_container')
            # print(len(TodayGames))
            # print(TodayGames[0].extract())
            LeagueItems = TodayGames[0].css('.eventlist_asia_fe_EventListLeague_container')
            print(len(LeagueItems))
            # if len(LeagueItems) == 0 :
            #     print('无数据，开始重新刷新网站！')
            #     self.driver.refresh()
            #     time.sleep(10)
            for league_item in LeagueItems:
                try:
                    # 获取联赛名称
                    league_name = league_item.css(".eventlist_asia_fe_EventListLeague_title").css("span::text").get()
                    print(league_name)
                    # 获取同一联赛下多场比赛
                    games = league_item.css('.eventlist_asia_fe_EventListLeague_singleEvent')
                    print(len(games))
                    for game in games:
                        try:
                            # 获取比分
                            score = game.css(".eventlist_asia_fe_sharedGrid_timeCell")
                            #print(score.extract())
                            score_text = score.css(".eventlist_asia_fe_EventTime_scoreLive").css("::text").get()
                            score_list = score_text.split(':')
                            print("主队得分：", score_list)
                            #print("客队得分：", score_text[2].css("span::text").get())

                            # 获取比赛时间
                            game_time = score.css(".eventlist_asia_fe_EventTime_gameProgress").css("span")
                            # print(game_time.extract())
                            print(game_time[0].css("span::text").get())
                            print(game_time[1].css("span::text").get())

                            # 获取多个盘口
                            oddsItems = game.css("div.eventlist_asia_fe_sharedGrid_eventLine.eventlist_asia_fe_sharedGrid_liveEvent")
                            print("盘口数量：", len(oddsItems))
                            # 球队名称
                            teamNames = oddsItems[0].css("span.eventlist_asia_fe_EventCard_teamNameText")
                            print("主队名称：", teamNames[0].css("span::text").get())
                            print("客队名称：", teamNames[1].css("span::text").get())

                            # 只获取第一个盘口
                            # 获取全场盘口
                            oddsColumn = oddsItems[0].css("div.eventlist_asia_fe_sharedGrid_verticalCellWrapper")
                            # 获取大小盘盘口
                            BigSmallColumn = oddsColumn.css("div.eventlist_asia_fe_sharedGrid_marketColumnWrapper.eventlist_asia_fe_sharedGrid_secondMarket")
                            #print(BigSmallColumn.extract())
                            outerOddsItems = BigSmallColumn.css("div.eventlist_asia_fe_sharedGrid_singleMarket")


                            # 让球数量
                            odds_text_wrap = outerOddsItems[0].css(".eventlist_asia_fe_sharedGrid_singleCell.eventlist_asia_fe_sharedGrid_singleLeftLive").css("span::text").get()
                            print("odds-text-wrap:", odds_text_wrap)
                            # 让球盘口
                            bigOdds = outerOddsItems[0].css(".eventlist_asia_fe_OddsArrow_oddsArrowNumber.eventlist_asia_fe_OddsArrow_oddsArrowNumberLive").css("span::text").get()
                            smallOdds = outerOddsItems[1].css(".eventlist_asia_fe_OddsArrow_oddsArrowNumber.eventlist_asia_fe_OddsArrow_oddsArrowNumberLive").css("span::text").get()
                            print("大：", bigOdds)
                            print("小：", smallOdds)

                            yield {
                                'time' : datetime.now(),
                                'league' : league_name,
                                'host' : remove_newlines(teamNames[0].css("span::text").get()),
                                'guest' : remove_newlines(teamNames[1].css("span::text").get()),
                                'quarter': game_time[0].css("span::text").get(),
                                'gameTime':  game_time[1].css("span::text").get(),
                                'hostScore': float(score_list[0]),
                                'guestScore': float(score_list[1]),
                                'bigSmall' : float(odds_text_wrap),
                                'bigOdds' : float(remove_newlines(bigOdds)),
                                'smallOdds' : float(remove_newlines(smallOdds)),
                                'firstQuarter': None,
                                'firstHalf': None,
                                'thirdQuarter': None,
                            }

                        except:
                            print('该赛事暂无盘口：', remove_newlines(teamNames[0].css("span::text").get()))
                except:
                    print('获取联赛名称失败。。。')
            #
            # time.sleep(3)