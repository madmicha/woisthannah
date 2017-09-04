import twitter
import json
import time
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#twitter credential (move later)
api = twitter.Api(consumer_key='uICny9VJBL5DSfpzjHJm9KZCD',
consumer_secret='VbzFdRm9NFnZFr8gsZvJj9IxUxtEZKgHWrIydW2eS8KDXPwTgm',
access_token_key='897347354554245120-ZrHM1Ksk0zg98z3YyagMVTfLINvPT5A',
access_token_secret='9SddyewS21DBmsUdsfIwlTzzDrTrZrIdut1Bct1HgSbKd')

#date

#nearest date
def nearest_date(items):
    return min(items, key=lambda x: abs(x - datetime.today()))
print(api.VerifyCredentials())

#crawl


settings = get_project_settings()
settings.overrides['FEED_FORMAT'] = 'jsonlines'
settings.overrides['FEED_URI'] = 'hannah_bookable_dates.jl'

process = CrawlerProcess(settings)

# 'followall' is the name of one of the spiders of the project.
process.crawl('hannah_v1', domain='hannah-lastenrad.de')
process.start() # the script will block here until the crawling is finished

time.sleep(1)

#load jsonlines
hannah_data = []
earliest_bookable_dates =[]

with open('hannah_bookable_dates.jl', 'r') as f:
    for line in f:
        if json.loads(line)['bookable_dates'] != []:
            earliest_bookable_dates.append(datetime.strptime(json.loads(line)['bookable_dates'][0],'%Y-%m-%d %H:%M:%S'))
        else:
        	   earliest_bookable_dates.append(datetime.strptime(json.loads(line)['location_timeframe'][-1],'%Y-%m-%d %H:%M:%S') + timedelta(days=1))
        hannah_data.append(json.loads(line))
#        
with open('hannah_bookable_dates.jl', 'w'): pass	
#print(earliest_bookable_dates)

next_bookable_hannahs =[]
for line in hannah_data:
	if line['bookable_dates'] == []:
	    pass
	else:
	    if datetime.strptime(line['bookable_dates'][0],'%Y-%m-%d %H:%M:%S')==nearest_date(earliest_bookable_dates):
	        next_bookable_hannahs.append("".join([" #",line['hannah_name'].replace(" ","")]))
if nearest_date(earliest_bookable_dates).date() == datetime.today().date():
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Heute gibt es noch ein kostenloses #Lastenrad in #Hannover"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('nnah')[1]])
    else:
        status_text = "".join(["Heute sind ",str(len(next_bookable_hannahs))," #Lastenrad in #Hannover buchbar:"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
else:
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Ein kostenloses #Lastenrad gibt es wieder am ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m.%y')," in #Hannover:"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('annah')[1]])
    else:
        status_text = "".join(["Schnapp dir ein #Lastenrad von ",str(len(next_bookable_hannahs))," in #Hannover wieder ab ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m'),":"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
print(status_text)
status = api.PostUpdate(status_text)
print(status.text)

#empty jl-file

