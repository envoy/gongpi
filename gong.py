#!/usr/bin/python
# 2014 Wells Riley
# 2017 Justin Ramos

import argparse
import pigpio
import time
import thread

parser = argparse.ArgumentParser(description='Strike dat gong.')
parser.add_argument('--pin', help='Servo GPIO pin; default 4', nargs='?',type=int, default=4)
parser.add_argument('--left', help='PWM left position; default 500', nargs='?',type=int, default=500)
parser.add_argument('--right', help='PWM right position; default 2500', nargs='?',type=int, default=2500)
parser.add_argument('--freq', help='PWM frequency in Hz; default 50', nargs='?',type=int, default=50)
parser.add_argument('--range', help='PWM frequency range; default 20000', nargs='?',type=int, default=20000)
parser.add_argument('--step', help='PWM step width; default 100', nargs='?',type=int, default=100)
parser.add_argument('--intensity', metavar='1-11', help='Step multiplier; default 1', nargs='?',type=int, default=1)

args = parser.parse_args()

PIN = args.pin
LEFT = args.left
RIGHT = args.right
CENTER = LEFT + ((RIGHT - LEFT)/2)
PWM_FREQ = args.freq
PWM_RANGE = args.range
PWM_STEP = args.step * args.intensity

pigpio = pigpio.pi()

def init_servo():
  pigpio.set_PWM_frequency(PIN, PWM_FREQ)
  pigpio.set_PWM_range(PIN, PWM_RANGE)
  move_servo(CENTER)

def move_servo(duty_cycle_us=0):
  pigpio.set_servo_pulsewidth(PIN, duty_cycle_us)

def spin_servo_cw_from(start, end):
  for duty_cycle_us in range(start, end+PWM_STEP, PWM_STEP):
    move_servo(duty_cycle_us)

def spin_servo_ccw_from(start, end):
  for duty_cycle_us in range(start, end-PWM_STEP, -PWM_STEP):
    move_servo(duty_cycle_us)

def stop_servo():
  move_servo(CENTER)
  pigpio.set_servo_pulsewidth(PIN, 0)

def gong():
  spin_servo_ccw_from(CENTER, LEFT)
  spin_servo_cw_from(LEFT, CENTER)

try:
  init_servo()
  gong()
  stop_servo()
finally:
  pigpio.stop()
