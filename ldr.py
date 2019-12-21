import os 
import redis
import time 

# Redis connection settings
# redis_host = os.environ.get('REDIS_HOST')
# redis_port = os.environ.get('REDIS_PORT')
# redis_password = os.environ.get('REDIS_PASSWORD')

redis_host = "localhost"
redis_port = 6379
redis_password = ""

class ldr: 
	def __init__(self, gpio, ldr_pin, redis_variable_name="LDR_VAL", reading_threshold=1): 
		self.GPIO = gpio 
		self.PIN = ldr_pin
		self.REDIS_VARIABLE = redis_variable_name
		self.TIME_THRESHOLD_FOR_READING = reading_threshold
  
		self.GPIO.setmode(self.GPIO.BOARD)
		self.GPIO.setwarnings(False)
		self.GPIO.setup(self.PIN, GPIO.OUT)
		self.GPIO.output(self.PIN, GPIO.LOW)
  
		self.MAX_DARK_INT = 20000
  
		# self.GPIO.setmode(self.GPIO.BOARD)
		# self.GPIO.setmode(self.GPIO.BOARD)
		# self.GPIO.setwarnings(False)
		# self.GPIO.setup(self.PIN, GPIO.OUT)
		# self.GPIO.output(self.PIN, GPIO.LOW)

		self.redis_connection = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

	def get_current_reading(self):
		"""
		Gets the current reading from the LDR
		"""
		count = 0
	
		#Output on the pin for 
		GPIO.setup(self.PIN, self.GPIO.OUT)
		GPIO.output(self.PIN, self.GPIO.LOW)
		time.sleep(0.1)

		#Change the pin back to input
		GPIO.setup(self.PIN, self.GPIO.IN)
	
		#Count until the pin goes high
		while (GPIO.input(self.PIN) == self.GPIO.LOW):
			count += 1

		return count
	
	def get_ldr_value(self):
		return self.redis_connection.get(self.REDIS_VARIABLE)

	def set_ldr_value(self):  
		start_time = time.time()
		readings_array = []
		while time.time() - start_time < self.TIME_THRESHOLD_FOR_READING: 
			readings_array.append(self.get_current_reading())
		if len(readings_array) == 0: 
			ldr_val = self.MAX_DARK_INT # Random maximum value if ldr cannot read value because of extra dark
		else:
			ldr_val = sum(readings_array)/len(readings_array)
		self.redis_connection.set(self.REDIS_VARIABLE, ldr_val)
		print(ldr_val)

if __name__ == '__main__': 
	import RPi.GPIO as GPIO
	obj = ldr(GPIO, 10)
	for i in range(100): 
		obj.set_ldr_value()
