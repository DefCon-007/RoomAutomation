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
		print (jsonData)
		publicUrl = jsonData["tunnels"][0]["public_url"]
		break
	except IndexError : 
		pass
# print (publicUrl)
if response.status_code == 200 : 
	htmlContent="""---
title: Room
layout: page
---

	<script type="text/javascript">
	        window.location.replace("{}");


	</script>

	"""
	with open("/home/pi/defcon-007.github.io/room.html","w") as f :
		f.write(htmlContent.format(publicUrl))
	call(["bash","commit.sh"])