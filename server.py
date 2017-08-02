#!/usr/bin/python
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
    data = web.data()
    ip = web.ctx['ip']

    # Write to the logfile
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f = open('/home/pi/gongpi/server.log','a')
    f.write('[' + ip + '] ' + timestamp + ': ' + data + '\n')
    f.close()

    try:
      server_json = json.loads(data)
    except ValueError, e:
      return '200 OK'

    print
    print '[' + ip + '] ' + server_json['type']

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
