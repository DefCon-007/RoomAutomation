"""
After the ngrok has started the tunnel
for the public URL this script updates 
my personal website with the URL. 
"""

import requests 
from subprocess import call 
sessionObj = requests.Session()

sessionObj.trust_env = False

while True:
	try : 
		response = sessionObj.get("http://127.0.0.1:4040/api/tunnels")
		jsonData = response.json()
		publicUrl = jsonData["tunnels"][0]["public_url"]
		break
	except IndexError : 
		pass

if response.status_code == 200 : 
	firstIndex = publicUrl.find("://")+3
	secondIndex = publicUrl.find(".")
	url = "https://api.keyvalue.xyz/71826813/roomurl/" + publicUrl[firstIndex: secondIndex]

	headers = {
	    'cache-control': "no-cache"
	    }

	response = requests.request("POST", url, headers=headers)