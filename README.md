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

**Note: These are *very* loose instructions to help get you started. This guide won't cover the basics of electronic wiring, Raspbian (the Raspberry Pi flavored Linux distro), and setting up a server to send webhooks from.**

1. Install [Raspbian](http://www.raspberrypi.org/).
2. Use the `raspi-config` menu to change the default password and set your time zone. **Don't skip this step.**
3. Once at the command prompt, run `sudo apt get update` and `sudo apt-get upgrade -y` to update your base system.
4. Run `apt-get install -y git python-pip pigpio`.
5. Clone the repo `git clone https://github.com/jramos/gongpi.git`.
6. `cd gongpi; sudo mv etc/rc.local /etc/rc.local; sudo chmod +x /etc/rc.local` – this overwrites the default rc.local with one that runs the required scripts on boot.
7. `pip install -r requirements.txt`.
8. Try running `sudo python server.py` – it should return the following:

  ```
  http://0.0.0.0:8080/
  ```

  If so, your webserver is now running and listening for incoming webhooks. You can test if incoming webhooks are correctly interprereted by running the following from **your machine** (not the Pi):

  ```
  curl -d '{"type":"charge.succeeded"}' [PI's IP ADDRESS]:8080
  ```

  Your servo should activate. `server.py` will print text in the console, and output an access log to `server.log`.

9. Restart your Pi `sudo shutdown -r now`
10. When the Pi reboots, it will automatically start the network monitor (which will auto-reconnect WiFi if disconnected), `pigpiod`, and the `server.py` server.
