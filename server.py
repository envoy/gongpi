#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2014 Wells Riley

import os
import web
import json
import RPi.GPIO as GPIO
import pigpio
import time

urls = ('/.*', 'hooks')
app = web.application(urls, globals())

PIN = 17
LEFT = 500
RIGHT = 2700
CENTER = LEFT + ((RIGHT - LEFT)/2)
STEP = 100
SLEEP = 0.02

pigpio_instance = pigpio.pi()

def start_servo():
  pigpio_instance.set_PWM_frequency(PIN, 50) # 50Hz pulses
  pigpio_instance.set_PWM_range(PIN, 20000) # 1,000,000 / 50 = 20,000us for 100% duty cycle
  move_servo(CENTER)

def stop_servo():
  move_servo(CENTER)
  pigpio_instance.set_servo_pulsewidth(PIN, 0)

def move_servo(duty_cycle_us=0):
  pigpio_instance.set_servo_pulsewidth(PIN, duty_cycle_us)
  time.sleep(SLEEP)

def spin_servo_cw_from(start, end):
  for duty_cycle_us in range(start, end + STEP, STEP):
    move_servo(duty_cycle_us)

def spin_servo_ccw_from(start, end):
  for duty_cycle_us in range(start, end-STEP, -STEP):
    move_servo(duty_cycle_us)

def gong():
  time.sleep(0.1)
  spin_servo_ccw_from(CENTER,LEFT)
  spin_servo_cw_from(LEFT,CENTER)

def do_gong():
  start_servo()
  gong()
  stop_servo()

def is_merged_to_master(json_payload):
  return json_payload['action'] == 'closed' and json_payload['pull_request']['merged'] and json_payload['pull_request']['base']['ref'] == 'master'

class hooks:
  def POST(self):
    data = web.data()

    try:
      json_payload = json.loads(data)
    except ValueError, e:
      return '200 OK'

    if is_merged_to_master(json_payload):
      do_gong()
    else:
      pass

    return '200 OK'

if __name__ == '__main__':
  try:
    app.run()
    do_gong()

  except KeyboardInterrupt:
    GPIO.cleanup()
    pigpio_instance.stop()
    app.stop()
