from flask import Flask,render_template
import json
import subprocess
procOut = subprocess.Popen(['osascript', '-'],
						 universal_newlines=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
procNoOut =  subprocess.Popen(['osascript', '-'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)

app = Flask(__name__)


@app.route('/getvolume')
def getVolume() :
	"""
		This function returns the current volume of the system. 

	"""
	scriptCode = """ output volume of (get volume settings) """
	# applescript.launch_script(scriptCode)
	stdout_output = procOut.communicate(scriptCode)[0]
	# print (stdout_output)
	return json.dumps({'success':True,"data":stdout_output}), 200, {'ContentType':'application/json'} 
# getVolume()

@app.route('/setvolume')
def setvolume():
	"""
		This function sets the volume to the sent amount

	"""
	scriptCode = "set volume output volume 59 --100%"
	procNoOut.communicate(scriptCode)


	
if __name__ == '__main__':
    app.run(port=8000)