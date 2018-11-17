from flask import Flask,render_template,request
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
from threading import Thread
import time 
import sys
import rgbStrip
import json
randomFlag = True

rbgObject = rgbStrip.rgb(GPIO)


rgbSmall = {
	"r" : 0,
	"g" : 0,
	"b" : 1
}

rgbLarge = {
	"r" : 0,
	"g" : 0,
	"b" : 1
}
monitorTop = [0,0,125]
monitorBottom = [0,0,125]
monitorLeft = [0,0,125]
monitorRight = [0,0,125]

timeOn = 0.05
timeOff = 0.08

pixels = rbgObject.pixels


def initialiseGPIO() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(11, GPIO.OUT) #For automating Solid State relay
	# GPIO.setup([r,g,b], GPIO.OUT, initial=GPIO.HIGH)

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
	rbgObject.setRGBSmall(rgbSmall["r"],rgbSmall["g"],rgbSmall["b"])
	rbgObject.setRGBLarge(rgbLarge["r"],rgbLarge["g"],rgbLarge["b"])
	setAllMonitor()


	# GPIO.output(b,0)

	# for i in range(pixels.count()): 
	# 	pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( 0,int(50),0 ))
	# pixels.show()
	return render_template("index.html",flag=1)
	
@app.route('/blueox')
def turnBlueOff() : 
	global randomFlag
	randomFlag = False
	rbgObject.clearAllMonitor()
	rbgObject.setRGBSmall(0,0,0)
	rbgObject.setRGBLarge(0,0,0)
	return render_template("index.html",flag=1)



# def flashrandomlightsmonitor() : 
# 	while randomFlag : 
# 		blink_color(pixels, blink_times = 1, color=(255, 0, 0))
# 		blink_color(pixels, blink_times = 1, color=(0, 255, 0))
# 		blink_color(pixels, blink_times = 1, color=(0, 0, 255))
# 	pixels.clear()
# 	pixels.show()

# def flashrandomlightsrgb() :
# 	GPIO.output(b,1)
# 	GPIO.output(r,1)
# 	GPIO.output(g,1)
# 	while randomFlag : 
# 		GPIO.output(r,0)
# 		time.sleep(0.08)
# 		GPIO.output(r,1)
# 		GPIO.output(b,0)
# 		time.sleep(0.08)
# 		GPIO.output(b,1)
# 		GPIO.output(g,0)
# 		time.sleep(0.08)
# 		GPIO.output(g,1)
def setAllMonitor() : 
	rbgObject.setMonitorTop(*monitorTop)
	rbgObject.setMonitorBottom(*monitorBottom)
	rbgObject.setMonitorLeft(*monitorLeft)
	rbgObject.setMonitorRight(*monitorRight)


def flashrandomlightsmonitor() : 
	while randomFlag : 
		setAllMonitor()
		rbgObject.setRGBSmall(rgbSmall["r"],rgbSmall["g"],rgbSmall["b"])
		rbgObject.setRGBLarge(rgbLarge["r"],rgbLarge["g"],rgbLarge["b"])
		time.sleep(timeOn)
		rbgObject.clearAllMonitor()
		rbgObject.setRGBSmall(0,0,0)
		rbgObject.setRGBLarge(0,0,0)
		time.sleep(timeOff)
		# blink_color(pixels, blink_times = 1, color=(255, 0, 0))
		# blink_color(pixels, blink_times = 1, color=(0, 255, 0))
		# blink_color(pixels, blink_times = 1, color=(0, 0, 255))
	# pixels.clear()
	# pixels.show()


@app.route('/randomcoloron')
def randomcolor() : 
	global randomFlag
	randomFlag = True
	t1 = Thread(target=flashrandomlightsmonitor)


	t1.start()

	return render_template("index.html",flag=1)
@app.route('/randomcoloroff') 
def randcoloroff() :
	global randomFlag 
	randomFlag = False
	return render_template("index.html",flag=1)
	return render_template("index.html",flag=1)

@app.route('/setColors', methods=["POST"])
def setAllColors() : 
	global monitorRight,monitorTop,monitorLeft,monitorBottom, timeOn, timeOff
	# data = request.data.split("&")
	data = json.loads(request.data)
	rgbS = data["rgbSmall"].split(",")
	
	rgbSmall["r"] = int(float(rgbS[0]))
	rgbSmall["g"] = int(float(rgbS[1]))
	rgbSmall["b"] = int(float(rgbS[2]))

	rgbL = data["rgbLarge"].split(",")
	rgbLarge["r"] = int(float(rgbL[0]))
	rgbLarge["g"] = int(float(rgbL[1]))
	rgbLarge["b"] = int(float(rgbL[2]))

	m = data["rgbmonitorTop"].split(",")
	# rbgObject.setMonitorTop
	monitorTop =  [int(float(m[0])), int(float(m[1])), int(float(m[2]))]
	m = data["rgbmonitorBottom"].split(",")
	monitorBottom = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]

	m = data["rgbmonitorLeft"].split(",")
	monitorLeft = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]
	
	m = data["rgbmonitorRight"].split(",")
	monitorRight = [int(float(m[0])), int(float(m[1])), int(float(m[2]))]

	timeOn = float(data["timeOn"])
	timeOff = float(data["timeOff"])
	setAllMonitor()
	print(m)
	return "ok"

def removeExtra() : 
	rbgObject.setMonitorExtra(0,0,0)

if __name__ == '__main__':
	t2 = Thread(target=removeExtra)
	t2.start()
	app.run(port=1234,debug=True)
