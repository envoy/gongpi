#!/bin/sh -e

# Ensure that the script has run on boot
sudo rm -rf /tmp/gonglord_log.txt
echo "Starting gonglord" > /tmp/gonglord_log.txt

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

# Kill PIGPIO daemon
kill pigpiod &

# Run PIGPIO daemon
/usr/local/bin/pigpiod &

# Run the webhook listener
python /home/pi/gonglord/server.py &

# Run the wifi connection monitor
sudo /home/pi/gonglord/network-monitor.sh &