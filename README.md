![gongpi](http://wellsosaur.us/YIA6/Untitled%20Sketch_bb.png)

# GongPi

Rings the gong in the Envoy office every time we make a sale.

[DEMO](http://wellsosaur.us/YFfX)

## Requirements

* RPi GPIO library
* [PIGPIO](http://abyz.co.uk/rpi/pigpio/) library
* Web.py
* Raspberry Pi (we used Adafruit Raspberry Pi Rev. B+)
* Internet connection (wired or wireless)
* Servo on GPIO pin 4
* One LED on GPIO pin 22

## Instructions

**Note: These are *very* loose instructions to help get you started. This guide won't cover the basics of electronic wiring, Raspbian (the Raspberry Pi flavored Linux distro), and setting up a server to send webhooks from.**

1. Install [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) – I recommend using NOOBS (linked) because it's easier.
2. Use the `raspi-config` menu to change the default password and set your time zone. **Don't skip this step.**
3. Once at the command prompt, run `apt get update` and `apt-get upgrade` to update your base system.
4. Run `apt-get install git`
5. Clone the repo `git clone git@github.com:envoy/gongpi.git`
6. `sudo mv rc.local /etc/rc.local` – this overwrites the default rc.local with one that runs the required scripts on boot.
6. Set up a cron on reboot of the raspberry pi - `sudo crontab -e`. Choose nano as your editor and add the line `@reboot /home/pi/gonglord/startup.sh`. This will instruct the raspberry pi to run gonglord upon boot. Add the line `chmod +x /home/pi/gonglord/startup.sh` to ensure the script is executable. Write out (ctrl + O) and ensure that the cron has written: `sudo crontab -l`.
7. [Install PIGPIO](http://abyz.co.uk/rpi/pigpio/download.html) – this gives us a Python library to easily control the servo.
8. `easy_install web.py` and `easy_install simplejson`
9. Try running `sudo python server.py` – it should return the following:

  ```
  http://0.0.0.0:8080/
  _
  ```

  If so, your webserver is now running and listening for incoming webhooks. You can test if incoming webhooks are correctly interprereted by running the following from **your machine** (not the Pi):

  ```
  curl -d '{"type":"charge.succeeded"}' [PI's IP ADDRESS]:8080
  ```

  The LED should start blinking, and your servo should activate. `server.py` will print text in the console, and output an access log to `server.log`.

10. Restart your Pi `sudo shutdown -r now`
11. When the Pi reboots, it will automatically start the network monitor (which will auto-reconnect WiFi if disconnected), `pigpiod`, and the `server.py` server.
