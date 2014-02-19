import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import openhab

from pyxbmct.addonwindow import *

class Radio:
	def __init__(self, label,id):
		self.label = label
		self.r = RadioButton('off')
		self.id = id

	def radio_update(self):
		if self.r.isSelected():
			self.r.setLabel('On')
			openhab.updateItem(openhab.Switch('ON', '', 'tutu aime les pommes', 'http://localhost:8080/rest/items/Light_FF_Bath_Ceiling'))
		else:
			self.r.setLabel('Off')
		
class MyWindow(AddonDialogWindow):

	def __init__(self, title, list):
		# You need to call base class' constructor.
		super(MyWindow, self).__init__(title)
		# Set the window width, height and the grid resolution: 9 rows, 4 columns.
		self.setGeometry(850, 550, 10,4)
		# Create a button.
		button = Button('Valider')
		# Place the button on the window grid.
		self.placeControl(button, 9,3)
		# Set initial focus on the button.
		self.setFocus(button)
		# Connect the button to a function.
		self.connect(button, self.close)
		self.set_active_controls(list)
		# Connect a key action to a function.
		self.connect(ACTION_NAV_BACK, self.close)
		
		self.test = xbmcgui.ControlSpin("salut")
		#self.test.addItem('1')
		#self.test.addItem('2')
		#spin = self.test.getSpinControl()
		self.addControl(self.test)

	def set_active_controls(self, list):
		# exemple RadioButton
		# self.radiobutton = RadioButton('Off')
		# self.placeControl(self.radiobutton, 6, 3)
		# self.connect(self.radiobutton, self.radio_update)
		
		self.radiobutton1 = Radio('Off',-1)
		self.placeControl(self.radiobutton1.r, 4, 2)
		self.connect(self.radiobutton1.r, self.radiobutton1.radio_update)
		
		self.radiobutton1 = Radio('Off',-2)
		self.placeControl(self.radiobutton1.r, 5, 2)
		self.connect(self.radiobutton1.r, self.radiobutton1.radio_update)
		
		self.i=1
		for item in list:
			label_label = Label(item.typeItem.label)
			#self.name = str(self.i)
			#print(self.name)
			self.tmp = Radio('On',self.i)
			if(self.i<7):
				self.placeControl(label_label, self.i, 0)
				self.placeControl(self.tmp.r, self.i, 1)
			else:
				self.placeControl(label_label, self.i, 2)
				self.placeControl(self.tmp.r, self.i, 3)
			self.connect(self.tmp.r, self.tmp.radio_update)
			self.i=self.i+1
			
	def generateListener(self,id):
		return ''
		
class Test(xbmcgui.WindowXML):
	def __init__(self, strXMLname, strFallbackPath, strDefaultName, forceFallback):
		pass
	def onInit(self):
		spin = getControl(5010)
#return super(WindowXML, cls).__new__(cls, 'test.xml', xbmcaddon.Addon(id=os.path.basename(os.getcwd()).getAddonInfo('path'),"Default","720p")