from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import scrapy
from scrapy_splash import SplashRequest


class Spider(scrapy.Spider):
    name = "hltvmatches"
    startDate = "&startDate=2021-01-01&endDate=2021-12-31"
    i = 0
    result = 0

    def start_requests(self):
        urls = [
            #&startDate=2019-08-14&endDate=2020-08-14
            'https://www.hltv.org/results?offset=1' + self.startDate
        ]

        for url in urls:
            return [SplashRequest(url=url, callback=self.parseNumber)]



    def parseNumber(self, response):
        open_in_browser(response)
        print("It works")
        self.result = int(response.xpath("//span[contains(concat(' ',normalize-space(@class),' '),' pagination-data ')]/text()").re_first('[0-9]+ $'))
        print(self.result)
        i = 0
        while i < self.result:
            yield SplashRequest(
                url = 'https://www.hltv.org/results?offset=' + str(i) + self.startDate,
                callback = self.parse,
                meta = {"index": str(i)},
            )
            i += 100

    def parse(self, response):
        results = response.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' result-con ')]/a/@href").getall()
        i = 0
        for result in results:
            i += 1
            yield SplashRequest(
                url = "https://www.hltv.org/" + result,
                callback = self.parseplayer,
                meta = {"index": str(int(response.meta["index"]) + i)},
            )


    def parseplayer(self, response):
        #open_in_browser(response)
        #//div[contains(concat(' ',normalize-space(@class),' '),' stats-content')]/table[contains(concat(' ',normalize-space(@class),' '),' table totalstats') and 1]//td/a/div/div[contains(concat(' ',normalize-space(@class),' '),' gtSmartphone-only statsPlayerName')]//text()
        team12players = response.xpath("//td[@class = 'player']/a/@href").getall()
        team1players = team12players[:5]
        team2players = team12players[5:]
        #team2players = response.xpath("//div[@id='all-content']/table[4]//tr[@class != 'header-row']//div[./span]//text()").getall()
        team1Score = response.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' team1-gradient ')]/div/text()").get()
        team2Score = response.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' team2-gradient ')]/div/text()").get()

        #print(str(team1players) + " " + str(team2players))
        # if team1players == []:
        #     open_in_browser(response)
        #     return
        # elif team2players == []:
        #     open_in_browser(response)
        #     return



        if len(team1players) > 10 and len(team1players) % 3 == 0:
            j = 0
            for i in range(0, len(team1players), 3):
                print(str(j) + " " + str(i))
                team1players[j] = team1players[i] + team1players[i + 1] + team1players[i + 2]
                j += 1
        if len(team2players) > 10 and len(team2players) % 3 == 0:
            j = 0
            for i in range(0, len(team2players), 3):
                print(str(j) + " " + str(i))
                team2players[j] = team2players[i] + team2players[i + 1] + team2players[i + 2]
                j += 1



        #print(str(team1players) + " : " + team1Score + "--" + team2Score + " : " + str(team2players) + " i: " + response.meta["index"])
        self.i += 1
        #print(str(self.i) + " / " + str(self.result))
        #self.ws['A' + str(index)] = team1
        #self.ws['B' + str(index)] = int(team1Score)
        #self.ws['D' + str(index)] = team2
        #self.ws['C' + str(index)] = int(team2Score)
        yield {
            "team1": team1players,
            "team2": team2players,
            "team1Score": team1Score,
            "team2Score": team2Score,
            "number": int(response.meta["index"])
        }
