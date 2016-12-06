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
