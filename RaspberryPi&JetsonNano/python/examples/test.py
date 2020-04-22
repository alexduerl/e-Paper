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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd4in2 Demo")
    
    epd = epd4in2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    logging.info("4.read bmp file on window")
    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, 'energy.bmp'))
    Himage2.paste(bmp, (50,10))
    epd.display(epd.getbuffer(Himage2))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()
