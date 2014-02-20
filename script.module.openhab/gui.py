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
		
class SliderUI:
	def __init__(self, item):
		self.item = item
		self.component = Slider()
		if item.typeItem.state == "Uninitialized":
			item.typeItem.state = 0
		self.label = Label(str(item.typeItem.state), alignment=ALIGN_CENTER)
	def update(self):
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

class Edit:
	def __init__(self, label):
		self.label = label
		self.edit = 0
	def update(self):
		if self.r.isSelected():
			self.r.setLabel('On')
			openhab.updateItem(openhab.Switch('ON', '', 'tutu aime les pommes', self.item.typeItem.link))
		else:
			self.r.setLabel('Off')
			openhab.updateItem(openhab.Switch('OFF', '', 'tutu aime les pommes', self.item.typeItem.link))
			

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
		# Connect a key action to a function.
		self.connect(ACTION_NAV_BACK, self.close)
		
		# affichage bouton en fonction du type
		self.set_active_controls(list)

	def set_active_controls(self, list):
		self.i=1
		for item in list:
			label_label = Label(item.typeItem.label)
			self.tmp = self.getUI(item)
			if(self.i<7):
				self.placeControl(label_label, self.i, 0)
				self.placeControl(self.tmp.component, self.i, 1)
			else:
				self.placeControl(label_label, self.i, 2)
				self.placeControl(self.tmp.component, self.i, 3)
			
			if self.tmp.__class__.__name__ == "SliderUI":
				self.placeControl(self.tmp.label, self.i,0.38)
				self.tmp.component.setPercent(float(item.typeItem.state))
				self.connectEventList([ACTION_MOVE_LEFT, ACTION_MOVE_RIGHT, ACTION_MOUSE_DRAG], self.tmp.update)
			elif self.tmp.__class__.__name__ == "LabelUI":
				pass
			else:
				self.connect(self.tmp.component, self.tmp.update)
			self.i=self.i+1
			
	def getUI(self, item):
		print(item.typeItem.__class__.__name__)
		if item.typeItem.__class__.__name__ == "Switch":
			return ButtonSwitch(item)
		if item.typeItem.__class__.__name__ == "RollerShutter":
			return SliderUI(item)
		if item.typeItem.__class__.__name__ == "Number":
			return LabelUI(item)
		if item.typeItem.__class__.__name__ == "Contact":
			return LabelUI(item)
		if item.typeItem.__class__.__name__ == "Dimmer":
			return SliderUI(item)
		# if item.typeItem.__class__.__name__ == "Color":
			# return SliderTriple(item)
		if item.typeItem.__class__.__name__ == "DateTime":
			return LabelUI(item)
		else:
			return LabelUI(item)