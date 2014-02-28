import xbmcplugin
import xbmcgui
import xbmc
import xbmcaddon
import openhab
from pyxbmct.addonwindow import * 

class ButtonSwitch:
	def __init__(self, item):
		self.item = item
		self.component = Button(self.item.typeItem.state)

	def update(self):
		if self.item.typeItem.state == "OFF":
			self.component.setLabel('ON')
			self.item.typeItem.state = "ON"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "ON":
			self.component.setLabel('OFF')
			self.item.typeItem.state = "OFF"
			openhab.updateItem(self.item)
	
class ButtonNumber:
	def __init__(self, item):
		self.item = item
		self.component = Button(self.item.typeItem.state)
	def update(self):
		if self.item.typeItem.state == "Uninitialized":
			self.component.setLabel('0')
			self.item.typeItem.state = "0"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "0":
			self.component.setLabel('25')
			self.item.typeItem.state = "25"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "25":
			self.component.setLabel('50')
			self.item.typeItem.state = "50"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "50":
			self.component.setLabel('75')
			self.item.typeItem.state = "75"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "75":
			self.component.setLabel('100')
			self.item.typeItem.state = "100"
			openhab.updateItem(self.item)
		elif self.item.typeItem.state == "100":
			self.component.setLabel('0')
			self.item.typeItem.state = "0"
			openhab.updateItem(self.item)
		else:
			self.component.setLabel('100')
			self.item.typeItem.state = "100"
			openhab.updateItem(self.item)
		
class SliderUI:
	def __init__(self, item):
		self.item = item
		self.component = Slider()
		if item.typeItem.state == "Uninitialized":
			self.item.typeItem.state = 0.0
			print 'IF'
		self.label = Label(str(item.typeItem.state), alignment=ALIGN_CENTER)
	def update(self):
		print 'UPDATE'
		try:
			self.item.typeItem.state = str(self.component.getPercent())
			self.label.setLabel('%.1f' % self.component.getPercent())
			openhab.updateItem(self.item)
		except (RuntimeError, SystemError):
			pass

class LabelUI:
	def __init__(self, item):
		self.item = item
		self.component = Label(self.item.typeItem.state)
	def update(self):
		pass

class MyWindow(AddonDialogWindow):

	def __init__(self, title, list):
		# You need to call base class' constructor.
		super(MyWindow, self).__init__(title)
		# Set the window width, height and the grid resolution: 9 rows, 4 columns.
		self.setGeometry(850, 550, 10,4)
		self.listUI = []
		# Create a button.
		buttonValidate = Button('Valider')
		# Place the button on the window grid.
		self.placeControl(buttonValidate, 9,3)
		# Set initial focus on the button.
		self.setFocus(buttonValidate)
		# Connect the button to a function.
		self.connect(buttonValidate, self.close)
		# Connect a key action to a function.
		self.connect(ACTION_NAV_BACK, self.close)
		
		#Navigation in the window
		self.set_active_controls(list)
		self.setNavigationItem()
		
		#Add Navigation link between listItem and Validate button
		buttonValidate.controlDown(self.listUI[0])
		buttonValidate.controlUp(self.listUI[len(self.listUI)-1])
		self.listUI[0].controlUp(buttonValidate)
		self.listUI[len(self.listUI)-1].controlDown(buttonValidate)

	def set_active_controls(self, list):
		self.i=1
		for item in list:
			label_label = Label(item.typeItem.label)
			self.tmp = self.getUI(item)
			if(self.i<8):
				self.placeControl(label_label, self.i, 0)
				self.placeControl(self.tmp.component, self.i, 1)
			else:
				self.placeControl(label_label, self.i%8+1, 2.25)
				self.placeControl(self.tmp.component, self.i%8+1, 3.25)
			
			if self.tmp.__class__.__name__ == "SliderUI":
				self.placeControl(self.tmp.label, self.i,0.38)
				self.tmp.component.setPercent(float(item.typeItem.state))
				self.connectEventList([ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT, ACTION_MOUSE_DRAG], self.tmp.update)
			elif self.tmp.__class__.__name__ == "LabelUI":
				pass
			else:
				self.connect(self.tmp.component, self.tmp.update)
			self.i=self.i+1
			if self.tmp.__class__.__name__ == "ButtonSwitch" or self.tmp.__class__.__name__ == "ButtonNumber":
				self.listUI.append(self.tmp.component)
		
	def getUI(self, item):
		print(item.typeItem.__class__.__name__)
		if item.typeItem.__class__.__name__ == "Switch":
			return ButtonSwitch(item)
		if item.typeItem.__class__.__name__ == "RollerShutter":
			return ButtonNumber(item)
		if item.typeItem.__class__.__name__ == "Number":
			return LabelUI(item)
		if item.typeItem.__class__.__name__ == "Contact":
			return LabelUI(item)
		if item.typeItem.__class__.__name__ == "Dimmer":
			return ButtonNumber(item)
		# if item.typeItem.__class__.__name__ == "Color":
			# return SliderTriple(item)
		if item.typeItem.__class__.__name__ == "DateTime":
			return LabelUI(item)
		else:
			return LabelUI(item)
			
	def setNavigationItem(self):
		for i in range(len(self.listUI)):
				if i < len(self.listUI)-1:
					self.listUI[i].controlDown(self.listUI[i+1])
				self.listUI[i].controlUp(self.listUI[i-1])
