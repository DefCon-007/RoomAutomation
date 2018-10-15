from flask import Flask,render_template
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO

b=32
r=33
g=12
PIXEL_COUNT = 49
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

import time 
import sys



def initialiseGPIO() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(11, GPIO.OUT) #For automating Solid State relay
	GPIO.setup([r,g,b], GPIO.OUT, initial=GPIO.HIGH)

	pixels.clear()
	pixels.show()  # Make sure to call show() after changing any pixels!

app = Flask(__name__)
initialiseGPIO()

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
	GPIO.output(b,0)

	for i in range(pixels.count()): 
		pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( 0,int(50),0 ))
	pixels.show()
	return render_template("index.html",flag=1)
	
@app.route('/blueox')
def turnBlueOff() : 
	GPIO.output(b,1)
	GPIO.output(r,1)
	GPIO.output(g,1)

	pixels.clear()
	pixels.show()
	return render_template("index.html",flag=1)

if __name__ == '__main__':

	app.run(port=1234)
