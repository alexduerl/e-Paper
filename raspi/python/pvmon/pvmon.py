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
temp = 0.0
hum = 0
production_day = 0.0
consumption_day = 0.0
self_consumption_day = 0.0
self_consumption_day_percent = 0
feedin_day = 0.0
feedin_day_percent = 0
purchased_day = 0.0
purchased_day_percent = 0
self_production_day = 0.0
self_production_day_percent = 0
storage_charge_level = 0
env_trees = 0
env_co2 = 0
sleep_time = 0

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2 Demo")

    epd = epd4in2.EPD()
    epd.init()

    connection_error = 300

    while True:

        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)

        url = 'http://homematic-raspi/addons/red/weather'
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
            sleep_time = 10

        url = 'http://homematic-raspi/addons/red/pvEnvBenefits'
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            env_trees = data["trees"]
            env_co2 = data["co2"]
        except requests.exceptions.RequestException as e:
            logging.error("Fehler: " + str(e))
            img = Image.open(os.path.join(picdir, 'alert.png'))
            Himage.paste(img, (185,273))
            sleep_time = 10

        url = 'http://homematic-raspi/addons/red/pvEnergyDay'
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            production_day = data["dayProduction"] / 1000
            consumption_day = data["dayConsumption"] / 1000
            feedin_day = data["dayFeedIn"] / 1000
            purchased_day = data["dayPurchased"] / 1000

            self_consumption_day = production_day - feedin_day
            feedin_day_percent = feedin_day / production_day * 100
            self_consumption_day_percent = 100 - feedin_day_percent

            self_production_day = consumption_day - purchased_day
            purchased_day_percent = purchased_day / consumption_day * 100
            self_production_day_percent = 100 - purchased_day_percent

        except requests.exceptions.RequestException as e:
            logging.error("Fehler: " + str(e))
            img = Image.open(os.path.join(picdir, 'alert.png'))
            Himage.paste(img, (185,273))
            sleep_time = 10

        url = 'http://homematic-raspi/addons/red/pvPowerFlow'
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            storage_charge_level = data["ChargeLevel"]

        except requests.exceptions.RequestException as e:
            logging.error("Fehler: " + str(e))
            img = Image.open(os.path.join(picdir, 'alert.png'))
            Himage.paste(img, (185,273))
            sleep_time = 10

        #logging.info("Temperature:" + str(temp))
        #logging.info("Humidity:" + str(hum))
        #logging.info("self_consumption:" + str(self_consumption_percent))
        #logging.info("feed:" + str(feed_percent)

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
        draw.text((45,232), str(('%.2f' % env_trees).replace('.', ',')), font = font24, fill = 0)

        img = Image.open(os.path.join(picdir, 'co2.png'))
        Himage.paste(img, (362,230))
        draw.text((245,232), str(('%.2f' % env_co2).replace('.', ','))+' kg', font = font24, fill = 0)

        # Produktion
        img = Image.open(os.path.join(picdir, 'self_consumption.png'))
        Himage.paste(img, (5,30))
        img = Image.open(os.path.join(picdir, 'feed.png'))
        Himage.paste(img, (362,30))
        img = Image.open(os.path.join(picdir, 'production.png'))
        Himage.paste(img, (120,30))
        #draw.text((170,30), '00,30', font = font24, fill = 0)
        #draw.text((230,30), 'kW', font = font24, fill = 0)
        draw.text((170,54), str(('%.2f' % production_day).replace('.', ','))+' kWh', font = font24, fill = 0)
        draw.text((5,75), str(int(self_consumption_day_percent)) +'%', font = font18, fill = 0)
        draw.text((355,75), str(int(feedin_day_percent))+'%', font = font18, fill = 0)
        draw.rectangle((48, 80, 351, 88), outline = 0)
        draw.rectangle((50, 83, 50+(self_consumption_day_percent*3), 85), fill = 0)
        draw.text((48, 90), 'Eigenverbrauch', font = font12, fill = 0)
        draw.text((285, 90), 'Einspeisung', font = font12, fill = 0)
        draw.text((48, 60), str(('%.2f' % self_consumption_day).replace('.', ',')), font = font18, fill = 0)
        draw.text((305, 60), str(('%.2f' % feedin_day).replace('.', ',')), font = font18, fill = 0)
        # Verbrauch
        img = Image.open(os.path.join(picdir, 'consumption.png'))
        Himage.paste(img, (120,105))
        #draw.text((170,105), '00,50', font=font24, fill = 0)
        #draw.text((230,105), 'kW', font=font24, fill = 0)
        draw.text((170,129), str(('%.2f' % consumption_day).replace('.', ','))+' kWh', font=font24, fill = 0)
        draw.text((5,150), str(int(self_production_day_percent))+'%', font = font18, fill = 0)
        draw.text((355,150), str(int(purchased_day_percent))+'%', font = font18, fill = 0)
        draw.rectangle((48, 155, 351, 163), outline = 0)
        draw.rectangle((50, 158, 50+(self_production_day_percent*3), 160), fill = 0)
        draw.text((48, 165), 'Eigenproduktion', font = font12, fill = 0)
        draw.text((315, 165), 'Zukauf', font = font12, fill = 0)
        draw.text((48, 135), str(('%.2f' % self_production_day).replace('.', ',')), font = font18, fill = 0)
        draw.text((315, 135), str(('%.2f' % purchased_day).replace('.', ',')), font = font18, fill = 0)

        # Battery
        img = Image.open(os.path.join(picdir, 'battery.png'))
        Himage.paste(img, (120,180))
        draw.text((170,180), str(storage_charge_level)+'%', font = font24, fill = 0)
        draw.rectangle((48, 210, 351, 218), outline = 0)
        draw.rectangle((50, 213, 50+(storage_charge_level*3), 215), fill = 0)

        # Last update
        draw.text((5,273), 'Stand: ' + now.strftime('%H:%M:%S'), font = font18, fill = 0)

        # Solaredge-Logo
        img = Image.open(os.path.join(picdir, 'solaredge.bmp'))
        Himage.paste(img, (275,273))
        draw = ImageDraw.Draw(Himage)

        epd.display(epd.getbuffer(Himage))
        time.sleep(sleep_time)
        #logging.info("Goto Sleep...")
        #epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
