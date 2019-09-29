from flask import Flask,render_template,request
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import os
import logging
from logdna import LogDNAHandler
from threading import Thread, Timer, Lock
import time 
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import sys
import rgbStrip
import json
import subprocess
from datetime import datetime as dt
from datetime import timedelta as td 
import atexit
randomFlag = True

log = logging.getLogger('logdna')
log.setLevel(logging.INFO)

options = {
  'hostname': 'roomAutomation',
}

# Defaults to False; when True meta objects are searchable
options['index_meta'] = True

test = LogDNAHandler(os.environ.get("LOGDNA_KEY"), options)

log.addHandler(test)


sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()]
)



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

PIN_FAN = 5
PIN_YELLOW_LIGHT = 3
PIN_WHITE_LIGHT = 11
PIN_BALCONY = 7

GPIO_LOW = 1
GPIO_HIGH = 0

PIR_ON = 1
PIR_OFF = 0

RELAY_PINS = [PIN_FAN, PIN_YELLOW_LIGHT, PIN_WHITE_LIGHT, PIN_BALCONY]
MOTION_INPUT_PIN = 8

LAST_UPDATED_TIME = dt.now()
TIME_THRESHOLD = 300

motion_sensor_thread = Thread()
motion_sensor_thread.start()
dataLock = Lock()


def create_app():
    app = Flask(__name__)

    def interrupt():
        global motion_sensor_thread
        motion_sensor_thread.cancel()

    def doStuff():
        global LAST_UPDATED_TIME
        global motion_sensor_thread

        with dataLock:
			# current_state = GPIO.input(MOTION_INPUT_PIN)
			# print("Tr ", current_state)
			if (dt.now() - LAST_UPDATED_TIME).total_seconds() > TIME_THRESHOLD: 
				current_state = GPIO.input(MOTION_INPUT_PIN)
				motion_sensor_action(current_state)
        # Do your stuff with commonDataStruct Here

        # Set the next thread to happen
        motion_sensor_thread = Timer(0.1, doStuff, ())
        motion_sensor_thread.start()   

    def doStuffStart():
        # Do initialisation stuff here
        global motion_sensor_thread
        # Create your thread
        yourThread = Timer(0.1, doStuff, ())
        yourThread.start()

    # Initiate
    doStuffStart()
    # When you kill Flask (SIGTERM), clear the trigger for the next thread
    atexit.register(interrupt)
    return app


app = create_app()


def initialise_GPIO_pins_for_relay(): 
	for pin in RELAY_PINS: 
		GPIO.setup(pin, GPIO.OUT)
		GPIO.output(pin, GPIO_LOW) # Start with all switches off

def initialiseGPIO() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
	initialise_GPIO_pins_for_relay()
	GPIO.setup(MOTION_INPUT_PIN, GPIO.IN)
    # GPIO.setup([r,g,b], GPIO.OUT, initial=GPIO.HIGH)
	pixels.clear()
	pixels.show()  # Make sure to call show() after changing any pixels!

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
 
def switch_relay(pin, state, is_pir_triggered=False): 
	global LAST_UPDATED_TIME
	if not is_pir_triggered: 
		LAST_UPDATED_TIME=dt.now()
	try : 
		GPIO.output(pin, state)
	except RuntimeError : 
		initialiseGPIO()
		GPIO.output(pin, state)


@app.route('/')
def index():
	return render_template('index.html',flag=0)
	# return "<h1>This flask app is running!</h1>"

@app.route('/nox')
def powerdown():
	switch_relay(PIN_WHITE_LIGHT, GPIO_LOW)
	return render_template("index.html",flag=1)

@app.route('/lumos')
def powerup():
	switch_relay(PIN_WHITE_LIGHT, GPIO_HIGH)
	return render_template("index.html",flag=1)


@app.route('/ventnox')
def fan_down():
	switch_relay(PIN_FAN, GPIO_LOW)
	return render_template("index.html",flag=1)

@app.route('/ventus')
def fan_on():
	switch_relay(PIN_FAN, GPIO_HIGH)
	return render_template("index.html",flag=1)


@app.route('/yelnox')
def yellowLightDown():
	switch_relay(PIN_YELLOW_LIGHT, GPIO_LOW)
	return render_template("index.html",flag=1)

@app.route('/yelos')
def yellowLightUp():
	switch_relay(PIN_YELLOW_LIGHT, GPIO_HIGH)
	return render_template("index.html",flag=1)


@app.route('/balnox')
def blaconyLightDown():
	switch_relay(PIN_BALCONY, GPIO_LOW)
	return render_template("index.html",flag=1)

@app.route('/balos')
def balconyLightUp():
	switch_relay(PIN_BALCONY, GPIO_HIGH)
	return render_template("index.html",flag=1)




# @app.route('/bluemos')
# def lightAllBlue() : 
# 	global randomFlag
# 	randomFlag = False
# 	rbgObject.setRGBSmall(rgbSmall["r"],rgbSmall["g"],rgbSmall["b"])
# 	rbgObject.setRGBLarge(rgbLarge["r"],rgbLarge["g"],rgbLarge["b"])
# 	setAllMonitor()
# 	t2 = Thread(target=removeExtra)
# 	t2.start()

# 	# GPIO.output(b,0)

# 	# for i in range(pixels.count()): 
# 	# 	pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color( 0,int(50),0 ))
# 	# pixels.show()
# 	return render_template("index.html",flag=1)
	
# @app.route('/blueox')
# def turnBlueOff() : 
# 	global randomFlag
# 	randomFlag = False
# 	rbgObject.clearAllMonitor()
# 	rbgObject.setRGBSmall(0,0,0)
# 	rbgObject.setRGBLarge(0,0,0)
# 	return render_template("index.html",flag=1)



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
	t2 = Thread(target=removeExtra)
	t2.start()

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


def motion_sensor_action(state): 
	"""
	Fan - 6 AM to 7 PM 
	White Light 7:01 PM to 12:00 AM 
	Yellow light : 12:01 AM to 5:59 AM
	"""
	AM_6 = dt.now().time().replace(hour=6, minute=0)
	PM_7 = dt.now().time().replace(hour=19, minute=0)
	AM_12 = dt.now().time().replace(hour=0, minute=0)
	current_time = dt.now().time()
	if state == PIR_ON: 
		if current_time >= AM_6 and current_time <= PM_7: 
			switch_relay(PIN_FAN, GPIO_HIGH, True)
		elif current_time > PM_7 and current_time <= AM_12 : 
			switch_relay(PIN_WHITE_LIGHT, GPIO_HIGH, True)
		elif current_time > AM_12 and current_time < AM_6: 
			switch_relay(PIN_YELLOW_LIGHT, GPIO_HIGH, True)


# def motion_sensor():
#     # Take action only after threshold seconds 
# 	global LAST_UPDATED_TIME
# 	try: 
# 		while True: 
			
# 	except KeyboardInterrupt: 
# 		GPIO.cleanup()

def removeExtra() : 
	print("In it")
	rbgObject.setMonitorExtra(0,0,0)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, debug=True)

    #subprocess.call(['./start-serveo.sh'])
