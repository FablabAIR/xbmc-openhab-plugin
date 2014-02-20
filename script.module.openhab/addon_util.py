import xbmcgui

def parseError(exceptionType, langage):
	errorId = 30004
	print exceptionType
	if exceptionType == "URLError":
		errorId += 1
	if exceptionType == "HTTPError":
		errorId += 2
	raiseError(langage(errorId))

def raiseError(errorText):
	xbmcgui.Dialog().ok("Error", errorText)
