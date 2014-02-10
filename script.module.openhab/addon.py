import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import urllib2
import json

#Global 
thisPlugin = int(sys.argv[1])

#Variable a recuperer dans les settings de XBMC 
#host ='localhost' 
#port ='8080'
#name ='demo'
#id = 'demo'

#Recuperation auto
__addon__      = xbmcaddon.Addon()
host = __addon__.getSetting('host')
port = __addon__.getSetting('port')
name = __addon__.getSetting('name')
id = __addon__.getSetting('id')

#Return Json from URL
def getJson(url) :
    json_string = urllib2.urlopen(url).read()
    data = json.loads(json_string)
    return data

#return SiteMap
def getJsonSiteMap(name,id):
    global host,port
    url = 'http://'+host+':'+port+'/rest/sitemaps/'+name+'/'+id+'?type=json'
    return getJson(url)

#return Item
def getJsonItem(item) :
    global host,port
    url = 'http://'+host+':'+port+'/rest/items/'+item+'?type=json'
    return getJson(url)


def createListing(data):
	listing = []
	widgets1 = data['widget']
	widgets2 = []

	for w in widgets1:
		widgets2.append(w['widget'])

	for floor in widgets2[0]:
		listing.append(floor['label'])

	return listing

def sendToXbmc(listing):
    global thisPlugin
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(thisPlugin,'',listItem)
    xbmcplugin.endOfDirectory(thisPlugin)

#Main 
siteMap = getJsonSiteMap(name,id);
listing = createListing(siteMap)
item = getJsonItem('Temperature_FF_Office')
print(item['state'])
listing.append(item['state'])
sendToXbmc(listing)
