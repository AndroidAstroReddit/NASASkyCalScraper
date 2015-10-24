# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SkycalscraperItem(scrapy.Item):
    month = scrapy.Field()
    day = scrapy.Field()
    day_of_week = scrapy.Field()
    #year is not necessary since the whole json file will be one year
    time = scrapy.Field()
    event = scrapy.Field()

