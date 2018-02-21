from kivy.uix.screenmanager import ScreenManager, Screen
import os

#Define phone Screen
class phoneHome(Screen):

	pass


class callScreen(Screen):

    def clearInputs(self):
        self.ids.number_input = ''

    def call(self,number):
        print('Calling phone')

        os.system('./vois_call.py ' + number) #Run python script to call

        #Clear inputs and return to home screen
        self.clearInputs()
        self.manager.transition.direction = 'right'
        self.manager.current = 'phoneHome'


class textScreen(Screen):

	def clearInputs(self):

		self.ids.number_input = ''
		self.ids.message_input = ''


	def text(self,number,message):
		print('Sending text message')

		print("number:", number)

		print("message:", message)

		os.system('./vois_text.py ' + number + ' ' + message) #Run python script to text

		#Clear inputs and return to call screen
		self.clearInputs()
		self.manager.transition.direction = 'right'
		self.manager.current = 'phoneHome'
