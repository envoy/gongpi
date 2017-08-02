#!/usr/bin/python
# 2014 Wells Riley, 2017 Justin Ramos

import pigpio
import time
import thread

PIN = 4
LEFT = 500
RIGHT = 2500
CENTER = LEFT + ((RIGHT - LEFT)/2)
STEP=100
SLEEP=0.01
PWM_FREQ=50      # 50Hz pulses
PWM_RANGE=20000  # 1,000,000 / 50 = 20,000us for 100% duty cycle

pigpio = pigpio.pi()

def init_servo():
  pigpio.set_PWM_frequency(PIN, PWM_FREQ)
  pigpio.set_PWM_range(PIN, PWM_RANGE)
  move_servo(CENTER)
  time.sleep(SLEEP)

def move_servo(duty_cycle_us=0):
  pigpio.set_servo_pulsewidth(PIN, duty_cycle_us)
  time.sleep(SLEEP)

def spin_servo_cw_from(start, end):
  for duty_cycle_us in range(start, end+STEP, STEP):
    move_servo(duty_cycle_us)

def spin_servo_ccw_from(start, end):
  for duty_cycle_us in range(start, end-STEP, -STEP):
    move_servo(duty_cycle_us)

def stop_servo():
  move_servo(CENTER)
  pigpio.set_servo_pulsewidth(PIN, 0)

def gong():
  init_servo()
  spin_servo_ccw_from(CENTER,LEFT)
  spin_servo_cw_from(LEFT,CENTER)
  stop_servo()
  pigpio.stop()

gong()
