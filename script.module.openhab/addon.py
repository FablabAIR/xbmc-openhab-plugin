import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import urllib2
import json
import urllib
import urlparse

####Fonctions ##########
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

     
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
 
#Main 

#Global 
 
base_url = sys.argv[0]
thisPlugin = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

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

#xbmc.executebuiltin('XBMC.RunScript("C:/Users/Jeff/AppData/Roaming/XBMC/addons/script.module.openhab/resources/lib/script.py")')
#siteMap = getJsonSiteMap(name,id);
#listing = createListing(siteMap)
#item = getJsonItem('Temperature_FF_Office')
#print(item['state'])
#listing.append(item['state'])
#sendToXbmc(listing)

 
#xbmcplugin.setContent(addon_handle, 'movies')

mode = args.get('mode', None)
 
if mode is None:
    siteMap = getJsonSiteMap(name,id)
    listing = createListing(siteMap)
    url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)

    #url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
    #li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
 
    #url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
    #li = xbmcgui.ListItem('Folder Two', iconImage='DefaultFolder.png')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)
 
    xbmcplugin.endOfDirectory(thisPlugin)
 
elif mode[0] == 'folder':
    #foldername = args['foldername'][0]
    #url = 'http://localhost/some_video.mkv'
    #li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    #xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    #xbmcplugin.endOfDirectory(addon_handle)
    listing = []
    item = getJsonItem('Temperature_FF_Office')
    listing.append(item['state'])

    url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
    li = xbmcgui.ListItem(item['state'], iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)
    #for item in listing:
    #    listItem = xbmcgui.ListItem(item)
    #    xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)