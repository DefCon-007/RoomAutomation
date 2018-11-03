from flask import Flask,render_template
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
from threading import Thread
import time 
import sys

b=32
r=33
g=12
PIXEL_COUNT = 49
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
randomFlag = True




def initialiseGPIO() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(11, GPIO.OUT) #For automating Solid State relay
	GPIO.setup([r,g,b], GPIO.OUT, initial=GPIO.HIGH)

	pixels.clear()
	pixels.show()  # Make sure to call show() after changing any pixels!

app = Flask(__name__)
initialiseGPIO()


def blink_color(pixels, blink_times=5, wait=0.5, color=(255,0,0)):
	for i in range(blink_times):
		# blink two times, then wait
		pixels.clear()
		for j in range(2):
			for k in range(pixels.count()):
				pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color( color[0], color[1], color[2] ))
			pixels.show()
			time.sleep(0.08)
			pixels.clear()
			pixels.show()
			time.sleep(0.08)
 

@app.route('/')
def index():
	return render_template('index.html',flag=0)
	# return "<h1>This flask app is running!</h1>"

@app.route('/nox')
def powerdown():
	try : 
		GPIO.output(11,1)
	except RuntimeError : 
		initialiseGPIO()
		GPIO.output(11,1)

	return render_template("index.html",flag=1)

@app.route('/lumos')
def powerup():
	try : 
		GPIO.output(11,0)
	except RuntimeError :
		initialiseGPIO()
		GPIO.output(11,0)
	return render_template("index.html",flag=1)

@app.route('/bluemos')
def lightAllBlue() : 
	global randomFlag
	randomFlag = False
	GPIO.output(b,0)

	for i in range(pixels.count()): 
		pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( 0,int(50),0 ))
	pixels.show()
	return render_template("index.html",flag=1)
	
@app.route('/blueox')
def turnBlueOff() : 
	global randomFlag
	randomFlag = False
	pixels.clear()
	pixels.show()
	GPIO.output(b,1)
	GPIO.output(r,1)
	GPIO.output(g,1)

	pixels.clear()
	pixels.show()
	return render_template("index.html",flag=1)



def flashrandomlightsmonitor() : 
	while randomFlag : 
		blink_color(pixels, blink_times = 1, color=(255, 0, 0))
		blink_color(pixels, blink_times = 1, color=(0, 255, 0))
		blink_color(pixels, blink_times = 1, color=(0, 0, 255))
	pixels.clear()
	pixels.show()

def flashrandomlightsrgb() :
	GPIO.output(b,1)
	GPIO.output(r,1)
	GPIO.output(g,1)
	while randomFlag : 
		GPIO.output(r,0)
		time.sleep(0.08)
		GPIO.output(r,1)
		GPIO.output(b,0)
		time.sleep(0.08)
		GPIO.output(b,1)
		GPIO.output(g,0)
		time.sleep(0.08)
		GPIO.output(g,1)

@app.route('/randomcoloron')
def randomcolor() : 
	global randomFlag
	randomFlag = True
	t1 = Thread(target=flashrandomlightsmonitor)
	t2 = Thread(target=flashrandomlightsrgb)

	t1.start()
	t2.start()
	return render_template("index.html",flag=1)
@app.route('/randomcoloroff') 
def randcoloroff() :
	global randomFlag 
	randomFlag = False
	return render_template("index.html",flag=1)
	return render_template("index.html",flag=1)
if __name__ == '__main__':

	app.run(port=1234)
