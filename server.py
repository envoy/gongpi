#!/usr/bin/python
# 2014 Wells Riley
# 2017 Justin Ramos

import argparse
import os
import web
import json
import time
from time import gmtime, strftime

# Catch the webhook
urls = ('/.*', 'hooks')
app = web.application(urls, globals())

class hooks:
  def logRequest(self, data):
    ip = web.ctx['ip']
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f = open('/home/pi/gongpi/server.log','a')
    f.write('[' + ip + '] ' + timestamp + ': ' + data + '\n')
    f.close()

  def POST(self):
    try:
      data = web.data()
      self.logRequest(data)
      server_json = json.loads(data)
    except ValueError, e:
      return '200 OK'

    if server_json['action'] == 'gong':
      intensity = server_json['intensity'] || 1
      os.system("python /home/pi/gongpi/gong.py --intensity {0}".format(intensity))
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
    app.stop()
