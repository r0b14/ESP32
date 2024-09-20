""" dht - modulo de temp e umidade """
import dht
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(17))
led = Pin(2, Pin.OUT)

while True:
  try:
    sleep(5)
    led.value(not led.value())
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    """ temp_f = temp * (9/5) + 32.0 """
    """ print('Temperature: %3.1f F' %temp_f) """
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
  except OSError as e:
    print('Failed to read sensor.')