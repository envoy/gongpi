#!/bin/sh -e

# Kill PIGPIO daemon
sudo kill pigpiod &

# Run PIGPIO daemon
sudo /usr/local/bin/pigpiod &

# Restart pagekite daemon
sudo invoke-rc.d pagekite restart

# Run the webhook listener
sudo python /home/pi/gonglord/server.py &

# Start pagekite
sudo pagekite.py 8080 gonglord.pagekite.me &

# Run the wifi connection monitor
sudo /home/pi/gonglord/network-monitor.sh &
