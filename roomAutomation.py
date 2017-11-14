from flask import Flask,render_template

try : 
	import RPi.GPIO as GPIO
	initialiseGPIO()
except : 
	pass

def initialiseGPIO() :
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(11, GPIO.OUT)
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
    # return "<h1>This flask app is running!</h1>"

@app.route('/lumos')
def tubelight():
	GPIO.output(11,1)
	return "<h1>Room in filled with Aura now !"

@app.route('/nox')
def lamp():
	GPIO.output(11,0)
	return "<h1> Death eaters are arriving !!"


if __name__ == '__main__':
    app.run(port=8000)
