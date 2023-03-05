# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyseleniumItem(scrapy.Item):
    # define the fields for your item here like:
    time = scrapy.Field()
    league = scrapy.Field()
    host = scrapy.Field()
    guest = scrapy.Field()
    bigSmall = scrapy.Field()
    bigOdds = scrapy.Field()
    smallOdds = scrapy.Field()

