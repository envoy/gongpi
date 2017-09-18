# GongPi

Rings the gong in the office every time we make a sale.

## Requirements

* Raspberry Pi
* Internet connection (wired or wireless)
* RC Servo

## Dependencies

* RPi GPIO library
* PIGPIO library
* Web.py

## Getting Started

```
sudo su -
apt-get install -y git python-pip pigpio
git clone https://github.com/jramos/gongpi.git
cd gongpi
mv etc/rc.local /etc/rc.local
chmod +x /etc/rc.local
pip install -r requirements.txt
/etc/rc.local
tail -f server.log
```

## JSON API

```
curl [PI's IP ADDRESS]:8080 -d '{
  "action":"gong",
  "intensity":1
}'
```

The servo will activate and strike the gong with the mallet at the specified intensity level.

## Gong Usage

```
$ python gong.py -h
usage: gong.py [-h] [--pin [PIN]] [--left [LEFT]] [--right [RIGHT]]
               [--freq [FREQ]] [--range [RANGE]] [--step [STEP]]
               [--intensity [1-11]]

Strike dat gong.

optional arguments:
  -h, --help          show this help message and exit
  --pin [PIN]         Servo GPIO pin; default 4
  --left [LEFT]       PWM left position; default 500
  --right [RIGHT]     PWM right position; default 2500
  --freq [FREQ]       PWM frequency in Hz; default 50
  --range [RANGE]     PWM frequency range; default 20000
  --step [STEP]       PWM step width; default 100
  --intensity [1-11]  Step multiplier; default 1
```
