#!/usr/bin/python
# Author: Suwat Saisema
# Date: 5-Oct-2017

import time

# Adafruit Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# MPD Clint
from mpd import MPDClient

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize Library
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
font_artist = ImageFont.truetype('arialuni.ttf', 14)
font_title = ImageFont.truetype('arialuni.ttf', 12)
font_info = ImageFont.truetype('arialuni.ttf', 10)

# Create drawing object.
draw = ImageDraw.Draw(image)
