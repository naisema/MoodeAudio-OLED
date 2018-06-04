# MoodeAudio-OLED
OLED 128x64 for MoodeAudio

![ScreenShot](https://github.com/naisema/MoodeAudio-OLED/blob/developer/OLED%20128x64.jpg?raw=true "OLED 128x64 Display")
<br />
Let see on Youtube <br />
[![OLED 128x64 Display](https://img.youtube.com/vi/ZFla1naHdzA/0.jpg)](https://www.youtube.com/watch?v=ZFla1naHdzA "OLED 126x64 Display")
<br />

Installation

1. Login to MoodeAudio with user pi and password moodeaudio
2. Ran raspi-config and enabled i2c
3. Prerequites <br />
   $ sudo apt-get update <br />
   $ sudo apt-get install build-essential python-pip python-dev python-smbus git python-imaging python-mpd<br />
4. Adafruit Python GPIO Library <br />
   $ git clone https://github.com/adafruit/Adafruit_Python_GPIO.git <br />
   $ cd Adafruit_Python_GPIO <br />
   $ sudo python setup.py install <br />
5. Adafruit Python SSD1306 <br />
   $ git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git <br />
   $ cd Adafruit_Python_SSD1306 <br />
   $ sudo python setup.py install <br />
6. Download python script from github <br />
   $ git clone https://github.com/naisema/MoodeAudio-OLED.git <br />
7. Go to MoodAudio UI menu -> Configure -> System -> Local Services -> LCD update engine
   fille full path of python script. On button and apply SET <br />
   ![ScreenShot](https://github.com/naisema/MoodeAudio-OLED/blob/developer/Python_LCD_setup.jpg?raw=true "Python LCD setup")
8. Display can show song information
