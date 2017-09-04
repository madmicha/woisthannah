# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HannahItem(scrapy.Item):
    # define the fields for your item here like:
    hannah_name = scrapy.Field()
    location_names  = scrapy.Field()
    location_gmaps_links = scrapy.Field()
    location_timeframe = scrapy.Field()
    bookable_dates = scrapy.Field()
    hannah_url = scrapy.Field()
    pass
