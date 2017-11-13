import json
import epd1in54
import time
import Image
import ImageDraw
import ImageFont
from datetime import datetime, timedelta


#date

#nearest date
def nearest_date(items):
    return min(items, key=lambda x: abs(x - datetime.today()))

def epdisplay(date,names,locations):
    header = date +": "+ str(len(names)) + " frei"
    epd = epd1in54.EPD()
    epd.init(epd.lut_full_update)
# For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (epd1in54.EPD_WIDTH, epd1in54.EPD_HEIGHT), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 12)
    draw.rectangle((0, 10, 200, 34), fill = 0)
    draw.text((8, 12), header, font = font, fill = 255)
    line_offset = 36
    for name,location in zip(names,locations):
        
        line = "".join([name,": ",location])
        draw.text((8, line_offset), line, font = font, fill = 0)
        line_offset += 15
    
    epd.clear_frame_memory(0xFF)
    epd.set_frame_memory(image, 0, 0)
    epd.display_frame()

    epd.delay_ms(2000)

#load jsonlines
hannah_data = []
earliest_bookable_dates =[]
not_bookable_hannahs = []

with open('hannah_bookable_dates.jl', 'r') as f:
    for line in f:
        if json.loads(line)['bookable_dates'] != []:
            earliest_bookable_dates.append(datetime.strptime(json.loads(line)['bookable_dates'][0],'%Y-%m-%d %H:%M:%S'))
        else:
            not_bookable_hannahs.append(json.loads(line)['hannah_name'])
        hannah_data.append(json.loads(line))
#        
#with open('hannah_bookable_dates.jl', 'w'): pass	
#print(earliest_bookable_dates)

next_bookable_hannahs =[]
next_bookable_hannahs_loc =[]
wann = None
for line in hannah_data:
	if line['bookable_dates'] == []:
	    pass
	else:
	    if datetime.strptime(line['bookable_dates'][0],'%Y-%m-%d %H:%M:%S')==nearest_date(earliest_bookable_dates):
	        next_bookable_hannahs.append(line['hannah_name'])
	        next_bookable_hannahs_loc.append("-".join(line['location_names']))
if nearest_date(earliest_bookable_dates).date() == datetime.today().date():
    wann = "Heute"
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Heute gibt es noch ein kostenloses #Lastenrad in #Hannover"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('nnah')[1]])
    else:
        status_text = "".join(["Heute sind ",str(len(next_bookable_hannahs))," #Lastenrad in #Hannover buchbar:"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
else:
    wann = datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m.%y')
    if len(next_bookable_hannahs)==1:
        status_text = "".join(["Ein kostenloses #Lastenrad gibt es wieder am ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m.%y')," in #Hannover:"]+next_bookable_hannahs+[' https://www.hannah-lastenrad.de/cb-items/hannah-',next_bookable_hannahs[0].split('annah')[1]])
    else:
        status_text = "".join(["Schnapp dir ein #Lastenrad von ",str(len(next_bookable_hannahs))," in #Hannover wieder ab ",datetime.strftime(nearest_date(earliest_bookable_dates),'%d.%m'),":"]+next_bookable_hannahs+[" https://www.hannah-lastenrad.de"])
print(status_text)
#DM to @madmicha
#message_text = "".join(["Tweetbot sagt Guten Morgen am ",datetime.strftime(datetime.today(),"%d.%m.%.y"),status_text])
#message = api.PostDirectMessage(u'madmicha',message_text)
#Post Status
#status = api.PostUpdate(status_text)
epdisplay(wann,next_bookable_hannahs,next_bookable_hannahs_loc)

#empty jl-file
with open('hannah_bookable_dates.jl', 'w'): pass
