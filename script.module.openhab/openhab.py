import json
import urllib
import urlparse
import urllib2

#Return Json from URL
def getJson(url) :
    json_string = urllib2.urlopen(url).read()
    data = json.loads(json_string)
    return data

#return SiteMap
def getJsonSiteMap(host, port, name, id):
    url = 'http://'+host+':'+port+'/rest/sitemaps/'+name+'/'+id+'?type=json'
    return getJson(url)

#return Item
def getJsonItem(item) :
    global host,port
    url = 'http://'+host+':'+port+'/rest/items/'+item+'?type=json'
    return getJson(url)
	
def updateItem(item):
	data = item.typeItem.state
	url = item.typeItem.link
	req = urllib2.Request(url, data, {'Content-Type': 'text/plain'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()

class Item:
	def __init__(self, id, label, link):
		self.id=id
		self.label=label
		self.link=link

# state value : on/off
class Switch(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# roller shutter value : unitialized (-1), 0-100
class RollerShutter(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# number value : int (affichage)
class Number(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# contact value : open/close
class Contact(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# dimmer value : unitialized (-1), 0-100
class Dimmer(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# color value : RGB (triple slider)
class Color(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# string value : string
class String(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# dateTime value : date
class DateTime(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state