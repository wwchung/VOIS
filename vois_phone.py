from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import os


def format(destination_number):
	return '+1 ' + destination_number[:3] + '-' + destination_number[3:6] + '-' + destination_number[6:]


#Define phone Screen
class PhoneScreen(Screen):
	pass


class CallScreen(Screen):

	labels = []
	
	def call(self, destination_number):
		self.labels[0].text = 'Calling ' + format(destination_number) + '...'
		os.system('./vois_call.py ' + destination_number)		# Run python script to call

	def reset_label(self):
		self.remove_label()
		lbl = Label(text='', font_size='56sp')
		self.labels.append(lbl)
		self.ids.box.add_widget(lbl)

	def remove_label(self):
		for lbl in self.labels:
			self.ids.box.remove_widget(lbl)
		self.labels.clear()


class TextScreen(Screen):

	labels = []

	def text(self, destination_number, message):
		self.labels[0].text = 'Sending ' + format(destination_number) + ':\n\n' + message
		os.system('./vois_text.py ' + destination_number + ' ' + message)		# Run python script to text

	def reset_label(self):
		self.remove_label()
		lbl = Label(text='', font_size='56sp')
		self.labels.append(lbl)
		self.ids.box.add_widget(lbl)

	def remove_label(self):
		for lbl in self.labels:
			self.ids.box.remove_widget(lbl)
		self.labels.clear()
