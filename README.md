![gongpi](http://wellsosaur.us/YIA6/Untitled%20Sketch_bb.png)

# Gonglord

Hits a gong when a pull request is accepted.

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
5. Clone the repo `git clone git@github.com:envoy/gongpi.git`
6. Set up a cron on reboot of the raspberry pi - `sudo crontab -e`. Choose nano as your editor and add the line `@reboot /home/pi/gonglord/startup.sh`. This will instruct the raspberry pi to run gonglord when it powers up. Add the line `chmod +x /home/pi/gonglord/startup.sh` to ensure the script is executable. Write out (ctrl + O) and ensure that the cron has been written: `sudo crontab -l`.
7. [Install PIGPIO](http://abyz.co.uk/rpi/pigpio/download.html) – this gives us a Python library to easily control the servo.
8. Install `server.py`'s dependencies: `easy_install web.py` and `easy_install simplejson`
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

## To connect external webhooks

Note, for this to work you will need to be a paid ngrok user.

1. Download pagekite: `cd ~ && curl -s https://pagekite.net/pk/ |sudo bash` - follow the instructions to register with pagekite
2. Install pagekite: `pagekite.py 8080 [your_unique_name].pagekite.me`
3. Configure pagekite to start when a network connection is established:

  ```bash
    sudo nano /etc/network/if-up.d/upstart
  ```

  Add the lines

  ```bash
    sudo pagekite.py 8080 [your_unique_name].pagekite.me
  ```

  Just below `all_interfaces_up()`. Your completed `all_interfaces_up()` method should look like this:

  ```bash
    all_interfaces_up() {
      sudo pagekite.py 8080 [your_unique_name].pagekite.me
      echo "Starting ngrok on $(date)" > /tmp/ngrok_log.txt
      # return true if all interfaces listed in /etc/network/interfaces as 'auto'
      # are up.  if no interfaces are found there, then "all [given] were up"
      local prefix="$1" iface=""
      for iface in $(get_auto_interfaces); do
        # if cur interface does is not up, then all have not been brought up
        [ -f "${prefix}${iface}" ] || return 1
      done
      return 0
    }
  ```

  Write out and reboot, `pagekite` should start.

4. Test it out!
  ```bash
    curl -d 'hello' https://[your_unique_name].pagekite.me/
  ```
