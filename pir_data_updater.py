from ldr import LDR
from redis_client import RedisCache
import time
import RPi.GPIO as GPIO
redis_connection = RedisCache()

PIR_GATE_PIN = 8
PIR_BED_PIN = 16 

#Set up gpio pin 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(PIR_GATE_PIN, GPIO.IN,  pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(PIR_BED_PIN, GPIO.IN,  pull_up_down = GPIO.PUD_DOWN)

while True:
    bed_value = GPIO.input(PIR_BED_PIN)
    gate_value = GPIO.input(PIR_GATE_PIN)
    if not gate_value:
        # Voltage is high(1) i.e. motion triggered
        redis_connection.set('PIR_GATE_PIN', time.time())
    
    if not bed_value: 
        redis_connection.set('PIR_BED_PIN', time.time())

GPIO.cleanup()