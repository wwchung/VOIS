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


def call(voice):

    outgoing = sys.argv[1]

    print("Calling: ", outgoing)

    voice.call('+1'+outgoing, '+17345854520')

def text(voice,outgoing,message):
    voice.send_sms('+1' + outgoing, message)


voice = Voice()
login(voice)

call(voice)
