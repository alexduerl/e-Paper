#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import requests
import datetime

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2 Demo")
    
    epd = epd4in2.EPD()
    epd.init()
    	
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    # Show Temperature and Humidity
    logging.info("1.Show Temperature and Humidity..")

    #bmp = Image.open(os.path.join(picdir, 'temp.png'))
    #Himage.paste(bmp, (5,22))

    while True:    
    	Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame


    	r = requests.get('http://homematic-raspi/addons/red/hello-json')
    	data = r.json()
    	temp = data["temperature"]
    	hum = data["humidity"]
    	logging.info("Temperature:" + str(temp))
    	logging.info("Humidity:" + str(hum)) 
    	
    	# Datum ermitteln
    	now = datetime.datetime.now()  
    	
    	# Solaredge-Logo
    	img = Image.open(os.path.join(picdir, 'solaredge.bmp'))
    	Himage.paste(img, (1,273))    	
    	draw = ImageDraw.Draw(Himage)
    	
    	# Temperature
    	img = Image.open(os.path.join(picdir, 'temp.bmp'))
    	Himage.paste(img, (1,273))    	
    	draw = ImageDraw.Draw(Himage)
    	
    	# Battery
    	img = Image.open(os.path.join(picdir, 'battery.png'))
    	Himage.paste(img, (270,273))    	
    	draw = ImageDraw.Draw(Himage)
    	draw.text((5, 0), now.strftime('%d.%m.%Y') + ' / ' + now.strftime('%H:%M'), font = font18, fill = 0)
    	draw.line((0, 25, 400, 25), fill = 0)
    	draw.line((0, 270, 400, 270), fill = 0)
    	draw.text((25, 22), 'Temperatur: ' +  str(temp) + '°C / ' + str(hum) + '%' , font = font24, fill = 0) 
    	epd.display(epd.getbuffer(Himage))
    	time.sleep(60)
    	#logging.info("Goto Sleep...")
    	#epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
