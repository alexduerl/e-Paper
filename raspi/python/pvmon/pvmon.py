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

# Fonts
font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)

#Variables
production = 60.0
self_consumption = 30.0
self_consumption_percent = 0
feed = 30.0
feed_percent = 0

self_consumption_percent = self_consumption / production * 100
feed_percent = feed / production * 100

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2 Demo")

    epd = epd4in2.EPD()
    epd.init()

    # Show Temperature and Humidity
    logging.info("1.Show Temperature and Humidity..")
    url = 'http://homematic-raspi/addons/red/hello-json'

    temp = 0.0
    hum = 0

    while True:

        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame

        try:

            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            temp = data["temperature"]
            hum = data["humidity"]
        except requests.exceptions.RequestException as e:
            logging.error("Fehler: " + str(e))
            img = Image.open(os.path.join(picdir, 'alert.png'))
            Himage.paste(img, (185,273))

        draw = ImageDraw.Draw(Himage)
        
        #logging.info("Temperature:" + str(temp))
        #logging.info("Humidity:" + str(hum))
        logging.info("self_consumption:" + str(self_consumption_percent))
        logging.info("feed:" + str(feed_percent)

        # Lines
        draw.line((0, 25, 400, 25), fill = 0)
        draw.line((0, 225, 400, 225), fill = 0)
        draw.line((0, 270, 400, 270), fill = 0)

        # Date
        now = datetime.datetime.now()
        draw.text((5, 0), now.strftime('%d.%m.%Y'), font = font24, fill = 0)

        # Temperature
        img = Image.open(os.path.join(picdir, 'temp.png'))
        Himage.paste(img, (225,0))
        draw = ImageDraw.Draw(Himage)
        draw.text((250, 0), str(temp) + '°C', font = font24, fill = 0)

        # Humidity
        img = Image.open(os.path.join(picdir, 'humidity.png'))
        Himage.paste(img, (325,0))
        draw = ImageDraw.Draw(Himage)
        draw.text((350, 0), str(hum) + '%' , font = font24, fill = 0)

        # Umwelt
        img = Image.open(os.path.join(picdir, 'trees.png'))
        Himage.paste(img, (5,230))
        draw.text((45,232), '445,13', font = font24, fill = 0)

        img = Image.open(os.path.join(picdir, 'co2.png'))
        Himage.paste(img, (205,230))
        draw.text((245,232), '14.919,75 kg', font = font24, fill = 0)

        # Produktion
        img = Image.open(os.path.join(picdir, 'self_consumption.png'))
        Himage.paste(img, (48,30))
        img = Image.open(os.path.join(picdir, 'feed.png'))
        Himage.paste(img, (319,30))
        img = Image.open(os.path.join(picdir, 'production.png'))
        Himage.paste(img, (120,30))
        draw.text((170,30), '00,30', font = font24, fill = 0)
        draw.text((230,30), 'kW', font = font24, fill = 0)
        draw.text((170,54), '60,00', font = font24, fill = 0)
        draw.text((230,54), 'kWh', font = font24, fill = 0)
        draw.text((5,75), str(int(self_consumption_percent)) +'%', font = font18, fill = 0)
        draw.text((355,75), str(int(feed_percent))+'%', font = font18, fill = 0)
        draw.rectangle((48, 80, 351, 88), outline = 0)
        draw.rectangle((50, 83, 50+(self_consumption_percent*3), 85), fill = 0)
        draw.text((48, 90), 'Eigenverbrauch', font = font12, fill = 0)
        draw.text((280, 90), 'Einspeisung', font = font12, fill = 0)
        draw.text((48, 66), '12 kWh', font = font12, fill = 0)
        draw.text((300, 66), '48 kWh', font = font12, fill = 0)
        # Verbrauch
        img = Image.open(os.path.join(picdir, 'consumption.png'))
        Himage.paste(img, (120,105))
        draw.text((170,105), '00,50', font=font24, fill = 0)
        draw.text((230,105), 'kW', font=font24, fill = 0)
        draw.text((170,129), '20,00', font=font24, fill = 0)
        draw.text((230,129), 'kWh', font=font24, fill = 0)
        draw.text((5,150), '80%', font = font18, fill = 0)
        draw.text((355,150), '20%', font = font18, fill = 0)
        draw.rectangle((48, 155, 351, 163), outline = 0)
        draw.rectangle((50, 158, 290, 160), fill = 0)
        draw.text((48, 165), 'Eigenproduktion', font = font12, fill = 0)
        draw.text((300, 165), 'Zukauf', font = font12, fill = 0)
        draw.text((48, 141), '16 kWh', font = font12, fill = 0)
        draw.text((300, 141), '4 kWh', font = font12, fill = 0)

        # Battery
        img = Image.open(os.path.join(picdir, 'battery.png'))
        Himage.paste(img, (120,180))
        draw.text((170,180), '50 %', font = font24, fill = 0)
        draw.rectangle((48, 210, 351, 218), outline = 0)
        draw.rectangle((50, 213, 200, 215), fill = 0)

        # Last update
        draw.text((5,273), 'Stand: ' + now.strftime('%H:%M:%S'), font = font18, fill = 0)

        # Solaredge-Logo
        img = Image.open(os.path.join(picdir, 'solaredge.bmp'))
        Himage.paste(img, (275,273))
        draw = ImageDraw.Draw(Himage)

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
