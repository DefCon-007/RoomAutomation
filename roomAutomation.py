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


if __name__ == '__main__':
    app.run(port=1234)
