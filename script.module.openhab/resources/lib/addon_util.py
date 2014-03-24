import xbmcgui
import urllib

## Documentation for raiseError.
	#@param exceptionType
	#@param langage : User language
#
#Display a dialog Error in XBMC

def parseError(exceptionType, langage):
	errorId = 30004
	print exceptionType
	if exceptionType == "URLError":
		errorId += 1
	if exceptionType == "HTTPError":
		errorId += 2
	xbmcgui.Dialog().ok("Error",langage(errorId))


## Documentation for log.
	#@param logText.
#
#Display a logText in XBMC log
def log(logText):
	print("[OpenHab]  " + logText)

## Documentation for build_url.
	#@param query.
	#@return Return the room list
#
#Create a XBMC query
def build_url(query,base_url):
    return base_url + '?' + urllib.urlencode(query)
 