import requests

### using http get request to get website

## Status code ( 2xx sucess) -- (4xx client problem)
## url itself
params = {"#q": "pizza"}
r = requests.get("https://google.com", params=params)
print("Status code:", r.status_code)
print(r.url)
## save gotten text in html file
f = open("./open.html", "w+")
f.write(r.text)


### using http get request to get IMAGE
from io import BytesIO
from PIL import Image

imageURL = "https://s1.1zoom.me/big0/861/Morning_Lake_Mountains_Austria_Steiermark_Fog_574162_1280x717.jpg"
r = requests.get(imageURL)
## Status code ( 2xx sucess) -- (4xx client problem)
print("Status code:", r.status_code)
## convert binaray content to Image
image = Image.open(BytesIO(r.content))
## print Image details 
print(image.size, image.format, image.mode)
## save Image
imgName = "image2"
imgPath = "./"+ imgName + "." + image.format 

try:
	image.save(imgPath, image.format)
except IOError:
	print("cannot save image")

'''
### using http post to post data to form 
# not work here need form..html and welcome.php
mydata = {"name": "Aliaa", "email": "aliaa@mail.com"}
r = requests.post("forexample\welcome.php", data=mydata)

## save gotten text in html file
f = open("./mt=yfile.html", "w+")
f.write(r.text) 
'''

'''
### using http post to post json data 
import simplejson as json

url = "googlr url shorthand which is deprected" #not work any more
payload = {"longUrl": "https://example.com/"} #domain
headers = {"Content-Type": "application/json"}
r = requests.post(url, json=payload, headers=headers)

print(r.text) # print json script of api state 

print(r.headers) # headers sent back from server
'''

