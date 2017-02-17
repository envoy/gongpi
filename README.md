![gongpi](http://wellsosaur.us/YIA6/Untitled%20Sketch_bb.png)

# Gonglord

Hits a gong when pushing to master.

## Requirements

* Raspberry Pi
* Internet connection (wired or wireless)
* Gong
* Servo on GPIO pin 4
* One LED on GPIO pin 22

## Optional

* Servo kit (I used Monk Makes Servo Kit for Raspberry Pi)
* Case for Raspberry Pi + Gong beater
* Beers

## Installation

**Note: These are *very* loose instructions to help get you started. This guide won't cover the basics of electronic wiring, Raspbian (the Raspberry Pi flavored Linux distro), and setting up webhooks.**

1. Install [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).
2. Use the `raspi-config` menu to change the default password and set your time zone. **Don't skip this step.**
3. Once at the command prompt, run `apt get update` and `apt-get upgrade` to update your base system.
4. Run `apt-get install git`
5. Clone the repo `git clone git@github.com:josephluck/gonglord.git`
6. Set up a cron on reboot of the raspberry pi - `sudo crontab -e`. Choose nano as your editor and add the line `@reboot /home/pi/gonglord/startup.sh`. This will instruct the raspberry pi to run gonglord on boot. Add the line `sudo chmod -R 0777 /home/pi/gonglord` to ensure the script is executable. Write out (ctrl + O) and ensure that the cron has been written: `sudo crontab -l`.
7. [Install PIGPIO](http://abyz.co.uk/rpi/pigpio/download.html) – this gives us a Python library to easily control the servo.
8. Install `server.py`'s dependencies: `easy_install web.py`
9. Try running `sudo python server.py` – it should return the following:

  ```
  http://0.0.0.0:8080/
  _
  ```

  If so, your webserver is now running and listening for incoming webhooks. You can test if incoming webhooks are correctly interprereted by running the following from **your machine** (not the Pi):

  ```
  curl -d '{"ref":"refs/head/master"}' [PI's IP ADDRESS]:8080
  ```

  Your servo should move.

10. Restart your Pi `sudo shutdown -r now`
11. When the Pi reboots, it will automatically start the network monitor (which will auto-reconnect WiFi if disconnected), `pigpiod`, `pagekite`, and the `server.py` server.

## To connect external webhooks

Note, for this to work you will need to be a paid ngrok user.

1. Register for pagekite: `https://pagekite.net/home/`
2. Set up pagekite: `https://pagekite.net/wiki/Howto/GNULinux/DebianPackage/`
3. Edit `startup.sh` in this repository to use your own unique pagekite subdomain
4. Set up pagekite to your credentials: `https://pagekite.net/wiki/Howto/GNULinux/ConfigureYourSystem/`
5. Test it out!
  ```bash
    curl -d '{"ref":"refs/head/master"}' [you_kite_name].pagekite.me:8080
  ```
6. Set up your 3rd party service to send webhook requests to your pagekite domain.
