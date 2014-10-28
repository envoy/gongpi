#!/usr/bin/python
# 2014 Wells Riley

import os
import web
import json
import RPi.GPIO as GPIO
import time
from threading import Thread

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

# Blink the LED 10 times – slooooooowly.
def BlinkSlow():
  for i in range(0,10):
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
    data = web.data()

    try:
      data_json = json.loads(data)

    except ValueError, e:
      return '200 OK'

    if data_json['type'] in ['charge.succeeded']:
      print
      print 'dolla dolla bills, yo!'
      print
      Thread(target=Blink).start()
      os.system("python /home/pi/gong.py 1")

    else:
      pass

    return '200 OK'

if __name__ == '__main__':
  try:
    app.run()

  except KeyboardInterrupt:
    print
    print "Exiting..."
    print
    GPIO.cleanup()
    pigpio.stop()
    app.stop()
