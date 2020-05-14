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

    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
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
        #temp = '21.9'
        #hum = '100'
        logging.info("Temperature:" + str(temp))
        logging.info("Humidity:" + str(hum))

        # Solaredge-Logo
        img = Image.open(os.path.join(picdir, 'solaredge.bmp'))
        Himage.paste(img, (275,273))
        draw = ImageDraw.Draw(Himage)

        # Datum
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

        # Produktion
        img = Image.open(os.path.join(picdir, 'production.png'))
        Himage.paste(img, (120,80))
        draw.text((170,100), '60.00 kWh', font = font24, fill = 0)
        draw.text((5,125), '20%', font = font18, fill = 0)
        draw.text((355,125), '80%', font = font18, fill = 0)
        draw.rectangle((48, 130, 351, 138), outline = 0)
        draw.rectangle((50, 133, 110, 135), fill = 0)
        draw.text((48, 140), 'Eigenverbrauch', font = font12, fill = 0)
        draw.text((280, 140), 'Einspeisung', font = font12, fill = 0)
        draw.text((48, 116), '12 kWh', font = font12, fill = 0)
        draw.text((300, 116), '48 kWh', font = font12, fill = 0)
        # Verbrauch
        img = Image.open(os.path.join(picdir, 'consumption.png'))
        Himage.paste(img, (120,150))
        draw.text((170,170), '17.02 kWh', font=font24, fill = 0)
        draw.text((5,195), '40%', font = font18, fill = 0)
        draw.text((355,195), '60%', font = font18, fill = 0)
        draw.rectangle((48, 200, 351, 208), outline = 0)
        draw.rectangle((50, 203, 170, 205), fill = 0)
        draw.text((48, 210), 'Eigenproduktion', font = font12, fill = 0)
        draw.text((300, 210), 'Zukauf', font = font12, fill = 0)

        # Aktuelle Leistung
        img = Image.open(os.path.join(picdir, 'power.png'))
        Himage.paste(img, (5,25))

        # Planted Trees
        img = Image.open(os.path.join(picdir, 'leaf.png'))
        Himage.paste(img, (180,220))

        # CO2 Footprint
        #img = Image.open(os.path.join(picdir, 'footprint.png'))
        #Himage.paste(img, (360,220))


        # Load
        img = Image.open(os.path.join(picdir, 'load.png'))
        Himage.paste(img, (205,25))

        # Battery
        img = Image.open(os.path.join(picdir, 'battery.png'))
        Himage.paste(img, (5,220))

        # Last update
        draw.text((5,273), 'Letztes Update: ' + now.strftime('%H:%M:%S'), font = font18, fill = 0)

        draw.line((0, 25, 400, 25), fill = 0)
        draw.line((0, 75, 400, 75), fill = 0)
        draw.line((200, 25, 200, 75), fill = 0)
        #draw.line((0, 220, 400, 220), fill = 0)
        draw.line((0, 270, 400, 270), fill = 0)

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
