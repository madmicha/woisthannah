import twitter 
import json 
import time 
from datetime import datetime, timedelta 
from scrapy.crawler import CrawlerProcess 
from scrapy.utils.project import get_project_settings

#twitter credential (move later)
execfile("twitter_cr3d3nt1als.py")

#date

#nearest date
def nearest_date(items):
    return min(items, key=lambda x: abs(x - datetime.today()))
print(api.VerifyCredentials())

#empty_jsonline    
with open('hannah_bookable_dates.jl', 'w'): pass	

#crawl
settings = get_project_settings()
settings.overrides['FEED_FORMAT'] = 'jsonlines'
settings.overrides['FEED_URI'] = 'hannah_bookable_dates.jl'

process = CrawlerProcess(settings)

# hannah_v1 is the name of one of the spiders of the project.
process.crawl('hannah_v1', domain='hannah-lastenrad.de')
process.start() # the script will block here until the crawling is finished

time.sleep(1)

#load jsonlines containing scraped data
hannah_data = []
earliest_bookable_dates =[]
not_bookable_hannahs = []


with open('hannah_bookable_dates.jl', 'r') as f:
    for line in f:
        print(line)
        if json.loads(line)['bookable_dates'] != []:
            earliest_bookable_dates.append(datetime.strptime(json.loads(line)['bookable_dates'][0],"%Y-%m-%d"))
        else:
            not_bookable_hannahs.append(json.loads(line)['hannah_name'])
        hannah_data.append(json.loads(line))



print(earliest_bookable_dates)
print(not_bookable_hannahs)

next_bookable_hannahs =[]
for line in hannah_data:
	if line['bookable_dates'] == []:
	    pass
	else:
	    if datetime.strptime(line['bookable_dates'][0],"%Y-%m-%d").date()==nearest_date(earliest_bookable_dates).date():
	        next_bookable_hannahs.append("".join([" #",line['hannah_name'].replace(" ","")]))
if nearest_date(earliest_bookable_dates).date() == datetime.today().date():
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Heute gibt es noch ein kostenloses #Lastenrad in #Hannover"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('nnah')[1]])
    if len(next_bookable_hannahs) != 1 and len(next_bookable_hannahs) < 6:
        today_bookable_hannahs =[]
        for bookable_hannah in next_bookable_hannahs:
            today_bookable_hannahs.append(bookable_hannah)
            today_bookable_hannahs.append(": https://www.hannah-lastenrad.de/cb-items/hannah-")
            today_bookable_hannahs.append(bookable_hannah.split('nnah')[1])
            today_bookable_hannahs.append("\n")
        status_text = "".join(["Heute sind noch ",str(len(next_bookable_hannahs))," kostenlose #Lastenrad frei: \n"]+today_bookable_hannahs)
    else:
        status_text = "".join(["Heute sind ",str(len(next_bookable_hannahs))," #Lastenrad in #Hannover buchbar:"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
else:
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Ein kostenloses #Lastenrad gibt es wieder am ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m.%y')," in #Hannover:"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('annah')[1]])
    if len(next_bookable_hannahs) != 1 and len(next_bookable_hannahs) < 6:
        someday_bookable_hannahs =[]
        for bookable_hannah in next_bookable_hannahs:
            print(bookable_hannah)
            someday_bookable_hannahs.append(bookable_hannah)
            someday_bookable_hannahs.append(": https://www.hannah-lastenrad.de/cb-items/hannah-")
            someday_bookable_hannahs.append(bookable_hannah.split('nnah')[1])
            someday_bookable_hannahs.append("\n")
        status_text = "".join(["Schnappt dir ein #Lastenrad von ",str(len(next_bookable_hannahs))," in #Hannover wieder ab ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m') ,": \n"]+someday_bookable_hannahs)
    else:
        status_text = "".join(["Schnapp dir ein #Lastenrad von ",str(len(next_bookable_hannahs))," in #Hannover wieder ab ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m'),":"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
print(status_text)
#DM to @madmicha
#message_text = "".join(["Tweetbot sagt Guten Morgen am ",datetime.strftime(datetime.today(),"%d.%m.%.y"),status_text])
#message = api.PostDirectMessage(u'madmicha',message_text)
#Post Status
status = api.PostUpdate(status_text,verify_status_length=False)
print(status.text)

#empty jl-file

