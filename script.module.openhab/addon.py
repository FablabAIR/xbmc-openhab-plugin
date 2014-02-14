import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import urllib2
import json
import urllib
import urlparse


class Node:
    #recupere info des etages
    def __init__(self, label, url, id, leaf):
        self.label = label
        self.url = url
        self.id = id
        self.leaf = leaf

class Leaf:
    #recupere info des etages
    def __init__(self, label, url, state, typeItem):
        self.label = label
        self.url = url
        self.state = state
        self.typeItem = typeItem



####Fonctions ##########
def log(str) :
        print("################[D] "+str+" ################")
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

def createListingSite(data):
    listing = []
    widgets1 = data['widget']
    widgets2 = []

    for w in widgets1:
        widgets2.append(w['widget'])
    
    for floor in widgets2[0]:
        tmp_floor = Node(floor['label'],floor['item']['link'], floor['linkedPage']['id'], floor['linkedPage']['leaf'])
        listing.append(tmp_floor)

    return listing


def createListingFloor(data):
	listing = []
	widgets = data['widget']

	for w in widgets:
			listing.append(Node(w['label'],w['item']['link'], w['linkedPage']['id'], w['linkedPage']['leaf']))

	return listing

def createListingRoom(data):
    listing = []
    widgets = data['widget']

    if type(widgets) is list:
        for w in widgets:
            listing.append(Leaf(w['label'],w['item']['link'], w['item']['state'], w['item']['type']))
    else :   
        listing.append(Leaf(widgets['label'],widgets['item']['link'], widgets['item']['state'], widgets['item']['type']))

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
DEBUG = __addon__.getSetting('Debug')
mode = args.get('mode', None)


if mode is None:
    log("Init")
    siteMap = getJsonSiteMap(name,id)
    listing = createListingSite(siteMap)
    
    for item in listing:
        if(item.leaf == 'false'):
            url = build_url({'mode': 'floor', 'id': item.id})
        else:
            url = build_url({'mode': 'room', 'id': item.id})
        listItem = xbmcgui.ListItem(item.label)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)
 
elif mode[0] == 'floor':
    log("Floor")
    id = args['id'][0]
    floor = getJsonSiteMap(name,id)
    listing = createListingFloor(floor)

    for item in listing:
        url = build_url({'mode': 'room', 'id': item.id})
        listItem = xbmcgui.ListItem(item.label)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)

elif mode[0] == 'room':
    log("Room")
    id = args['id'][0]
    room = getJsonSiteMap(name, id)
    listing = createListingRoom(room)

    for item in listing:
        listItem = xbmcgui.ListItem(item.label)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url='',listitem=listItem, isFolder=False)
    xbmcplugin.endOfDirectory(thisPlugin)
