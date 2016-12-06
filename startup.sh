#!/bin/sh -e

# Ensure that the script has run on boot
sudo echo "Starting gonglord on $(date)" > /tmp/gonglord_log.txt

# Kill PIGPIO daemon
sudo kill pigpiod &

# Run PIGPIO daemon
sudo /usr/local/bin/pigpiod &

# Run the webhook listener
sudo python /home/pi/gonglord/server.py &

# Run the wifi connection monitor
sudo /home/pi/gonglord/network-monitor.sh &
