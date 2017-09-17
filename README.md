# GongPi

Rings the gong in the office every time we make a sale.

## Requirements

* RPi GPIO library
* PIGPIO library
* Web.py
* Raspberry Pi
* Internet connection (wired or wireless)
* Servo on GPIO pin 4

## Instructions

```
sudo su -
apt-get install -y git python-pip pigpio
git clone https://github.com/jramos/gongpi.git
cd gongpi
mv etc/rc.local /etc/rc.local
chmod +x /etc/rc.local
pip install -r requirements.txt
/etc/rc.local
```

You can test if incoming webhooks are correctly interpreted by running the following from another computer:

```
curl -d '{"action":"gong", "intensity":1}' [PI's IP ADDRESS]:8080
```

The servo should activate.

Reboot the Pi, and the server will start automatically. The access log can be found in `server.log`.
