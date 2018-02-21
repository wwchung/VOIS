#!/usr/bin/python
# GOOGLE VOICE NUMBER ----------- 734-506-8603 -----------


from googlevoice import Voice
from googlevoice.util import input

import sys

def login(voice):
    username, password = "eecs498.vois@gmail.com", "umichvois"
    print("Logging in...")

    client = voice.login(username, password)
    return client


def text(voice):
    outgoing = sys.argv[1] #Get outgoing number
    message = sys.argv[2:] #Get message
    message = ' '.join(message) #Turn message into string
    voice.send_sms('+1' + outgoing, message) #Send message


voice = Voice() #Create new voice object
login(voice) #Login to google Account
text(voice) #Send text message 
