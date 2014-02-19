import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import os.path
import xbmc
import urllib2
import json
import urllib
import urlparse
import openhab
import gui

# To recover info of floors and rooms
class Node:
    def __init__(self, label, url, id, leaf):
        self.label = label
        self.url = url
        self.id = id
        self.leaf = leaf

# To recover info of sentors
class OpenHabItem:
	def __init__(self, label, url, state, typeItem, id):
		self.typeItem = self.defItem(label, url, state, typeItem, id)
	def defItem(self, label, link, state, typeItem, id):
		if typeItem == "SwitchItem":
			return openhab.Switch(state, id, label, link)
		elif typeItem == "RollerShutterItem":
			return openhab.RollerShutter(state, id, label, link)
		elif typeItem == "NumberItem":
			return openhab.Number(state, id, label, link)
		elif typeItem == "ContactItem":
			return openhab.Contact(state, id, label, link)
		elif typeItem == "DimmerItem":
			return openhab.Dimmer(state, id, label, link)
		elif typeItem == "ColorItem":
			return openhab.Color(state, id, label, link)
		elif typeItem == "DateTimeItem":
			return openhab.DateTime(state, id, label, link)
		else:
			return openhab.Switch(state, id, label, link)

####Fonctions ##########

# Fonction log
def log(str) :
	print("################[D] "+str+" ################")

# Creer la liste des etages
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

# Creer la liste des pieces dans les etages
def createListingFloor(data):
	listing = []
	widgets = data['widget']

	for w in widgets:
			listing.append(Node(w['label'],w['item']['link'], w['linkedPage']['id'], w['linkedPage']['leaf']))

	return listing

# Creer la liste des capteurs dans les pieces (item)
def createListingRoom(data):
    listing = []
    widgets = data['widget']

    if type(widgets) is list:
        for w in widgets:
            listing.append(OpenHabItem(w['label'],w['item']['link'], w['item']['state'], w['item']['type'], w['widgetId']))
    else :   
        listing.append(OpenHabItem(widgets['label'],widgets['item']['link'], widgets['item']['state'], widgets['item']['type'], w['widgetId']))

    return listing
     
# Construit l'url
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
 
#Main 

# Info global 
base_url = sys.argv[0]
thisPlugin = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

# Recuperation auto dans les settings de XBMC 
__addon__      = xbmcaddon.Addon()
host = __addon__.getSetting('host')
port = __addon__.getSetting('port')
name = __addon__.getSetting('name')
id = __addon__.getSetting('id')
DEBUG = __addon__.getSetting('Debug')
mode = args.get('mode', None)

# Navigation dans les menus
if mode is None:
    log("Init")
    siteMap = openhab.getJsonSiteMap(host, port, name, id)
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
    floor = openhab.getJsonSiteMap(host, port, name, id)
    listing = createListingFloor(floor)

    for item in listing:
        url = build_url({'mode': 'room', 'id': item.id, 'label':item.label})
        listItem = xbmcgui.ListItem(item.label)
        xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)
    xbmcplugin.endOfDirectory(thisPlugin)

elif mode[0] == 'room':
	log("Room")
	id = args['id'][0]
	label = args['label'][0]
	room = openhab.getJsonSiteMap(host, port, name, id)
	listing = createListingRoom(room)
	#window = gui.MyWindow(label, listing)
	window = gui.Test("test.xml", os.getcwd(), "Default", "720p")
	window.doModal()