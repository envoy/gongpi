#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2014 Wells Riley

import os
import web
import json
import RPi.GPIO as GPIO
import time
from threading import Thread
from time import gmtime, strftime

# Set up LED on GPIO pin 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22,False)

# Blink the LED 10 times
def Blink():
  for i in range(0,20):
    GPIO.output(22,True)
    time.sleep(0.125)
    GPIO.output(22,False)
    time.sleep(0.125)

# Blink the LED 5 times – slowly.
def BlinkSlow():
  for i in range(0,5):
    GPIO.output(22,True)
    time.sleep(1)
    GPIO.output(22,False)
    time.sleep(1)

# Blink to indicate the server is listening
Thread(target=BlinkSlow).start()

# Catch the webhook
urls = ('/.*', 'hooks')
app = web.application(urls, globals())

class hooks:
  def POST(self):
    ip = web.ctx['ip']
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    serverlog = open('/home/pi/gonglord/server.log','a')

    # Write to the logfile
    serverlog.write('Received hook from: ' + ip + ' at: ' + timestamp + '\n')
    serverlog.close()

    # Make some noises
    print
    print 'drop da bass'
    print
    Thread(target=Blink).start()
    os.system("python /home/pi/gonglord/gong.py 1")

    return '200 OK'

if __name__ == '__main__':
  try:
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    serverlog = open('/home/pi/gonglord/server.log','a')
    serverlog.write('Server starting: ' + timestamp + '\n')
    serverlog.close()
    app.run()

  except KeyboardInterrupt:
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    serverlog = open('/home/pi/gonglord/server.log','a')
    serverlog.write('Server stopping: ' + timestamp + '\n')
    serverlog.close()
    print
    print "Exiting..."
    print
    GPIO.cleanup()
    pigpio.stop()
    app.stop()
