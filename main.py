# Development board: D1 mini 
# Development environment: Micropython

# Including
from machine import Pin, Timer, PWM
import time

# Initialization
BrePin = Pin(13, Pin.OUT)
BrePin.value(0)
BreLED = PWM(BrePin, 1000)
LED = Pin(2, Pin.OUT)
PIR = Pin(5, Pin.IN)
LED.value(1)
BreLED.duty(0)

# Definition of variable
step   = 32
_duty  = 0
ms     = round(3000 / step) # Unit in microsecond
state  = False
start_timer = True
delay_ms = 6 * 1000
ii = 0


def breath(t):
  global step, _duty
  _duty += step
  
  if _duty > 1023:
    _duty = 1023
    step *= -1
  elif _duty < 0:
    _duty = 0
    step *= -1
  BreLED.duty(_duty)

try:
  while True:
    if PIR.value() == 1:      
      if (state == False):
        LED.value(0)
        tim = Timer(-1)
        tim.init(period = ms, mode = Timer.PERIODIC, callback = breath) 
        print('Motion detected.')
        print(ii)   
        ii += 1
        state = True
    if state:
      if start_timer:
        start = time.ticks_ms()
        start_timer = False
        
      delta = time.ticks_diff(time.ticks_ms(),start) 
      
      if delta >= delay_ms:
        start_timer = True
        state = False
        LED.value(1)
        BreLED.duty(0)
        tim.deinit()
        print('LED truns off.')

except KeyboardInterrupt:
  tim.deinit()
  LED.deinit()
  ledPin.value(0)
  print('-----Stop-----')

