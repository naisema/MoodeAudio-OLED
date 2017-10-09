# MoodeAudio-OLED
OLED 128x64 for MoodeAudio


Copy moode-oled.service to /lib/systemd/system

sudo chmod 644 /lib/systemd/system/hello.service
chmod +x /home/pi/MoodeAudio-OLED/moode-oled.py
sudo systemctl daemon-reload
sudo systemctl enable moode-oled.service
sudo systemctl start moode-oled.service
