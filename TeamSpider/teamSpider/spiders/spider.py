from scrapy.selector import Selector
from scrapy.utils.response import open_in_browser
import scrapy
from openpyxl import load_workbook


class Spider(scrapy.Spider):
    name = "hltvTeams"

    wb = load_workbook(filename='players2012-2020.xlsx')
    ws = wb['PlayersRating']

    hashPlayers = {}
    for player in ws.rows:
        hashPlayers[player[0].value] = player[1].value

    def start_requests(self):
        urls = ['https://www.hltv.org' + player for player in self.hashPlayers]
        print(len(urls))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = response.xpath("//div[@class = 'playerTeam']//a/@href").get()
        if result is None:
            result = response.xpath("//span[contains(concat(' ',normalize-space(@class),' '),' profile-player-stat-value bold ')]//a/@href").get()

        if result is not None:
            yield scrapy.Request(
                url = "https://www.hltv.org" + result,
                callback = self.parseTeam
            )


    def parseTeam(self, response):
        teamPlayers = response.xpath("//div[contains(concat(' ',normalize-space(@class),' '),' bodyshot-team g-grid ')]/a/@href").getall()
        teamName = response.xpath("//h1[contains(concat(' ',normalize-space(@class),' '),' profile-team-name text-ellipsis ')]/text()").get()

        teamELOReturn = []
        for player in teamPlayers:
            try:
                teamELOReturn.append(self.hashPlayers[player])
            except:
                print("Player: " + player + " was not saved")
                teamELOReturn.append(0)
            try:
                self.hashPlayers.pop(player, None)
            except:
                pass
        yield {
            "team": teamPlayers,
            "teamELO": teamELOReturn,
            "teamName": teamName
        }
