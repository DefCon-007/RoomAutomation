import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


PIXEL_COUNT = 46
SPI_PORT   = 0
SPI_DEVICE = 0

RGB_ON = 0
RGB_OFF = 1


RGB_SMALL_R = 33
RGB_SMALL_B = 32
RGB_SMALL_G = 12

RGB_LARGE_R = 38
RGB_LARGE_G = 40
RGB_LARGE_B = 36

STRIP_EXTRA = range(5)
STRIP_BOTTOM = range(5,19)
STRIP_RIGHT = range(19,26)
STRIP_TOP = range(26,39)
STRIP_LEFT = range(39,46)

class rgb : 

	def __init__(self, gpio, pixelCount = 49) :
		self.GPIO = gpio
		self.GPIO.setmode(self.GPIO.BOARD)
		self.GPIO.setwarnings(False)

		self.GPIO.setup([RGB_LARGE_R, RGB_LARGE_G, RGB_LARGE_B, RGB_SMALL_R, RGB_SMALL_G, RGB_SMALL_B ], self.GPIO.OUT, initial=self.GPIO.HIGH)
		self.pixels = Adafruit_WS2801.WS2801Pixels(pixelCount, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=self.GPIO)
		# self.p = self.pixels
	# def clearAll() : 
	def convertRGB(self, r,g,b) : 
		r = RGB_ON if r else RGB_OFF
		b= RGB_ON if b else RGB_OFF
		g = RGB_ON if g else RGB_OFF 
		return (r,g,b)

	def setRGBSmall(self,r,g,b) : 
		r,g,b = self.convertRGB(r,g,b)

		self.GPIO.output(RGB_SMALL_R, r)
		self.GPIO.output(RGB_SMALL_B, b)
		self.GPIO.output(RGB_SMALL_G, g)
		
	def setRGBLarge(self,r,g,b) : 
		r,g,b = self.convertRGB(r,g,b)

		self.GPIO.output(RGB_LARGE_R, r)
		self.GPIO.output(RGB_LARGE_B, b)
		self.GPIO.output(RGB_LARGE_G, g)

	def setAllMonitor(self, r,g,b,includeExtra = False) :
		if includeExtra :
			self.setMonitorExtra(r,g,b)

		self.setMonitorLeft(r,g,b)
		self.setMonitorRight(r,g,b)
		self.setMonitorTop(r,g,b)
		self.setMonitorBottom(r,g,b)

		self.pixels.show()

	def clearAllMonitor(self) : 
		self.pixels.clear()
		self.pixels.show()

	def setMonitorExtra(self,r,g,b) : 
		for k in STRIP_EXTRA : 
			self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( r,b,g ))
		self.pixels.show()

	def setMonitorLeft(self,r,g,b) : 
		for k in STRIP_LEFT : 
			self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( r,b,g ))
		self.pixels.show()

	def setMonitorRight(self,r,g,b) : 
		for k in STRIP_RIGHT : 
			self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( r,b,g ))
		self.pixels.show()

	def setMonitorTop(self,r,g,b) : 
		for k in STRIP_TOP : 
			self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( r,b,g ))
		self.pixels.show()

	def setMonitorBottom(self,r,g,b) : 
		for k in STRIP_BOTTOM : 
			self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( r,b,g ))
		self.pixels.show()		