from ldr import LDR
from redis_client import RedisCache

redis_connection = RedisCache()

LDR_PIN = 10
LDR_VAR_NAME = 'LDR_BED'

ldr_obj = LDR(LDR_PIN)

while True:
    value = ldr_obj.get_ldr_value()
    print("The value is ", value)
    redis_connection.set(LDR_VAR_NAME, value)
    
GPIO.cleanup()