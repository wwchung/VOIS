from pynput.keyboard import Key, Controller
import time

#Takes control of the keyboard and changes the application that is focused
keyboard = Controller()

switch = True

#Will rotate through open applications. Switches every five seconds to leave time for voice commands
with keyboard.pressed(Key.cmd):

	while switch:
		keyboard.press(Key.tab)
		keyboard.release(Key.tab)

		#Insert check for stop command

		time.sleep(5)

