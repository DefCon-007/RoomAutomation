import os
import time 
import multiprocessing

class LDR: 
    def __init__(self, ldr_pin, gpio=None, ldr_reading_threshold=1, accuracy_time_threshold=1.5): 
        if not gpio: 
            import RPi.GPIO as GPIO
            
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            self.GPIO = GPIO
        else: 
            self.GPIO = gpio 
        self.PIN = ldr_pin
        self.TIME_THRESHOLD_FOR_READING = ldr_reading_threshold
        self.ACCURACY_THRESHOLD = accuracy_time_threshold
  
        # self.GPIO.setmode(self.GPIO.BOARD)
        # self.GPIO.setwarnings(False)
        self.GPIO.setup(self.PIN, GPIO.OUT)
        self.GPIO.output(self.PIN, GPIO.LOW)
  
        self.MAX_DARK_INT = 1000000

    def get_current_reading(self):
        """
        Gets the current reading from the LDR
        Returns integer where 0 -> brightest, -1 -> unable to completely take reading because of darkness
        """
        count = 0
        start_time = time.time()
    
        #Output on the pin for 
        self.GPIO.setup(self.PIN, self.GPIO.OUT)
        self.GPIO.output(self.PIN, self.GPIO.LOW)
        time.sleep(0.1)

        #Change the pin back to input
        self.GPIO.setup(self.PIN, self.GPIO.IN)
    
        #Count until the pin goes high
        while (self.GPIO.input(self.PIN) == self.GPIO.LOW):
            count += 1
            if time.time() - start_time >= self.TIME_THRESHOLD_FOR_READING: 
                return -1
        return count

    def get_ldr_value(self):  
        """
        Morning no light average value = 30 
        """
        start_time = time.time()
        ldr_value = None
        readings_array = []
        while time.time() - start_time < self.ACCURACY_THRESHOLD: 
            current_reading = self.get_current_reading()
            if current_reading == -1: 
                ldr_value = self.MAX_DARK_INT
                break
            else:
                readings_array.append(current_reading)
        if not ldr_value:
            ldr_value = sum(readings_array)/len(readings_array)
        return ldr_value
