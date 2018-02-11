# -*- coding: utf-8 -*-
import scrapy
import locale
import time
from datetime import datetime
#import datetime
locale.setlocale(locale.LC_ALL,("de_DE.utf8"))
#Helper Functions to parse the given date-format (German Months, without explicit year given )
from dateutil import parser
from dateutil.relativedelta import relativedelta

def parse_future(timestr, **parse_kwargs):
    """Same as dateutil.parser.parse() but only returns future dates."""
    now = datetime.now()
    try:
        dt = parser.parse(timestr, parserinfo=GermanParserInfo(), **parse_kwargs)
    except ValueError:
        pass
    if dt > now: # original date is in future
        pass
    else:
        dt += relativedelta(years=+1)
    if dt > now: # future date is one year later
        pass
    else:
        print("No Future date found")
    return dt

class GermanParserInfo(parser.parserinfo):
    MONTHS = [
        ('Jan'),('Feb'),('Mrz'),('Apr'),('Mai'),('Jun'),('Jul'),('Aug'),('Sep'),('Okt'),('Nov'),('Dez'),
    ]
#testdate = datetime.date(2013,3,3)
#print(testdate.strftime("%d.%b %Y"))
class HannahSpider(scrapy.Spider):
    name = 'hannah_v1'
    allowed_domains = ['hannah-lastenrad.de']
    start_urls_prefix = "https://www.hannah-lastenrad.de/cb-items/hannah-"
    start_urls = []
    for i in range(1,19):
        start_url = ''.join([start_urls_prefix,str(i),'//'])
        start_urls.append(start_url)
    #start_urls = ['http://https://www.hannah-lastenrad.de//']

    def parse(self, response):
        print "URL: " + response.url
        #print(response.xpath('//li[contains(@class, "bookable")]//span/text()').extract())
        bookable_dates_iterator = iter(response.xpath('//li[contains(@class, "bookable")]//span/text()').extract())
        bookable_dates = [c.zfill(3) +' ' +next(bookable_dates_iterator,'') for c in bookable_dates_iterator]
        bookable_dates = [''.join([t,'2018']) for t in bookable_dates]
        print(list(bookable_dates))
        try:
            print(bookable_dates)
            print(bookable_dates_iterator)
            bookable_date_parsed = [parse_future(t) for t in bookable_dates]
            print(bookable_date_parsed)
        except:
            print("mooep")
        time.sleep(1)
        
        location_timeframend = [x[-8:] for x in response.xpath("//span[@class='cb-date']/text()").extract()]
     
        yield {
        'hannah_name': response.xpath('//h1/text()').extract_first(),
        'location_names': [x.strip() for x in response.xpath("//div[@class='cb-location-name cb-big']/text()").extract()],
        'location_gmaps_links': [x.strip() for x in response.xpath("//div[@class='cb-address cb-row']/a/@href").extract()],
        'location_timeframe': [parse_future(t) for t in [x.strip() for x in location_timeframend]],
        'bookable_dates': [parse_future(t) for t in bookable_dates]
        }
        pass
        
        #[datetime.strptime(t, '%d.%m.%Y') for t in 
