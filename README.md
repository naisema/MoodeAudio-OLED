# MoodeAudio-OLED
OLED 128x64 for MoodeAudio


Copy moode-oled.service to /lib/systemd/system <br />

sudo chmod 644 /lib/systemd/system/hello.service <br />
chmod +x /home/pi/MoodeAudio-OLED/moode-oled.py <br />
sudo systemctl daemon-reload <br />
sudo systemctl enable moode-oled.service <br />
sudo systemctl start moode-oled.service <br />
