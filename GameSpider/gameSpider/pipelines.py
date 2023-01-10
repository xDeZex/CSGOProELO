# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook

class XlsxPipeline(object):
    """Save scraped data to an XLSX spreadsheet"""
    i = 0

    def open_spider(self, spider):
        """Start scraping"""
        # Create an Excel workbook
        self.wb = Workbook(write_only=True)
        self.ws = self.wb.create_sheet()
        self.ws.title = "Matches"

    def process_item(self, item, spider):
        # Append a row to the spreadsheet
        row = []
        for player in item["team1"]:
            row.append(player)
        if len(row) != 5:
            for x in range(0, 5 - len(row)):
                row.append(None)
        row.append(int(item["team1Score"]))
        row.append(int(item["team2Score"]))
        for player in item["team2"]:
            row.append(player)
        if len(row) != 12:
            for x in range(0, 12 - len(row)):
                row.append(None)
        row.append(int(item["number"]))
        self.ws.append(row)
        self.i += 1
        return item

    def close_spider(self, spider):
        """Stop scraping"""
        # Save the Excel workbook
        self.wb.save('matches2021.xlsx')

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TutorialPipeline:
    def process_item(self, item, spider):
        return item
