#!/bin/sh -e

# Ensure that the script has run on boot
echo "Starting gonglord on $(date)" > /tmp/gonglord_log.txt &

# Kill PIGPIO daemon
kill pigpiod &

# Run PIGPIO daemon
/usr/local/bin/pigpiod &

# Start pagekite
sudo pagekite.py 8080 [your_unique_name].pagekite.me &

# Run the webhook listener
python /home/pi/gonglord/server.py &

# Run the wifi connection monitor
sudo /home/pi/gonglord/network-monitor.sh &
