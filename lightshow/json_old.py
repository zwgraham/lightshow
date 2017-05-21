import simplejson
from urllib2 import Request, urlopen, URLError

request = Request('https://jsonplaceholder.typicode.com/posts/1')

try:
	response = urlopen(request)
	#kittens = response.read()
	#print kittens
	#print kittens

	jsonData = response.read()
	jsonDataPython = simplejson.loads(jsonData)
	print jsonDataPython['title']
except URLError, e:
	print 'No kittez. Got an error code:',e
