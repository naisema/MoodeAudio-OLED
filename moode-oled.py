#!/usr/bin/python
# Author: Suwat Saisema
# Date: 5-Oct-2017

import sys
import time
import os

# Adafruit Library
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# MPD Clint
from mpd import MPDClient, MPDError, CommandError, ConnectionError

# System UTF-8
reload(sys)
sys.setdefaultencoding('utf-8')

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# MPD Client
class MPDConnect(object):
    def __init__(self, host='localhost', port=6600):
        self._mpd_client = MPDClient()
        self._mpd_client.timeout = 10
        self._mpd_connected = False

        self._host = host
        self._port = port

    def connect(self):
        if not self.connected:
            try:
                self._mpd_client.ping()
            except(socket_error, ConnectionError):
                try:
                    self._mpd_client.connect(self._host, self._port)
                    self.connected = True
                except(socket_error, ConnectionError, CommandError):
                    self.connected = False

    def disconnect(self):
        self._mpd_client.close()
        self._mpd_client.disconnect()

    def _play_pause(self):
        self._mpd_client.pause()
        #return False

    def _next_track(self):
        self._mpd_client.next()
        #return False

    def _prev_track(self):
        self._mpd_client.previous()
        #return False

    def fetch(self):
        # MPD current song
        song_info = self._mpd_client.currentsong()

        # Artist Name
        if 'artist' in song_info:
            artist = song_info['artist']
        else:
            artist = 'Unknown Artist'
        # Song Name
        if 'title' in song_info:
            title = song_info['title']
        else:
            title = 'Unknown Title'

        # MPD Status
        song_stats = self._mpd_client.status()
        # State
        state = song_stats['state']

        # Song time
        if 'elapsed' in song_stats:
            elapsed = song_stats['elapsed']
            m,s = divmod(float(elapsed), 60)
            h,m = divmod(m, 60)
            eltime = "%d:%02d:%02d" % (h, m, s)
        else:
            eltime ="0:00:00"

        # Audio
        if 'audio' in song_stats:
            bit = song_stats['audio'].split(':')[1]
            frequency = song_stats['audio'].split(':')[0]
            z, f = divmod( int(frequency), 1000 )
            if ( f == 0 ):
                frequency = str(z)
            else:
                frequency = str( float(frequency) / 1000 )
            bitrate = song_stats['bitrate']

            audio_info =  bit + "bit " + frequency + "kHz " + bitrate + "kbps"
        else:
            audio_info = ""

        # Volume
        vol = song_stats['volume']

        return({'state':state, 'artist':artist, 'title':title, 'eltime':eltime, 'volume':int(vol), 'audio_info':audio_info})

def main():
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
    font_artist = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Arial-Unicode-Bold.ttf', 14)
    font_title = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Arial-Unicode-Regular.ttf', 13)
    font_info = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Verdana-Italic.ttf', 10)
    font_time = ImageFont.truetype('/home/pi/MoodeAudio-OLED/Verdana.ttf', 13)

    # Create drawing object.
    draw = ImageDraw.Draw(image)

    # First define some constants to allow easy resizing of shapes.
    padding = 2
    shape_width = 20
    top = padding
    bottom = height-padding
    artoffset = 2
    titoffset = 2
    animate = 15

    # MPD Connect
    client = MPDConnect()
    client.connect()

    # Draw data to display
    while True:
        # Clear image buffer by drawing a black filled box.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Fetch data
        info = client.fetch()
        state = info['state']
        eltime = info['eltime']
        vol = info['volume']
        artist = info['artist']
        title = info['title']
        audio = info['audio_info']

        # Position text of Artist
        artwd,artz = draw.textsize(unicode(artist), font=font_artist)

	# Artist animate
	if artwd < width:
            artx = (width - artwd) / 2
	    artoffset = padding
        else:
            artx = artoffset
            #artoffset -= animate
            #if (artwd - (width + abs(artx))) < -120:
            #    artoffset = 100

        # Position text of Title
        titwd,titz = draw.textsize(unicode(title), font=font_title)

	# Title animate
	if titwd < width:
            titx = (width - titwd) / 2
	    titoffset = padding
        else:
            titx = titoffset
            titoffset -= animate
	    if (titwd - (width + abs(titx))) < -120:
		titoffset = 100

        # Position text of audio infomation
        audiox,audioy = draw.textsize(audio, font=font_info)
        if audiox < 126:
            audiox,audioy = divmod((126-audiox),2)
        else:
            audiox = 2

        if state == 'stop':
            # Draw text
            draw.text((30,15), "Music Stop", font=font_title, fill=255)
            draw.text((padding,50), eltime, font=font_time, fill=255)
            draw.text((75,50), "vol: " +  str(vol) , font=font_time, fill=255)
        else:
            # Draw text.
            draw.text((artx,top), unicode(artist), font=font_artist, fill=255)
            draw.text((titx,18), unicode(title), font=font_title, fill=255)
            draw.text((audiox,35), audio, font=font_info, fill=255)
            draw.text((padding,50), eltime, font=font_time, fill=255)
            draw.text((75,50), "vol: " +  str(vol) , font=font_time, fill=255)

        # Draw the image buffer.
        disp.image(image)
        disp.display()

        # Pause briefly before drawing next frame.
        time.sleep(1)

if __name__ == "__main__":
    main()
