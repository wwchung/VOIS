#!/usr/bin/python
import pickle
import os

class ContactBook:

    def __init__(self, filename = "~/contacts.p"):
        self.filename = filename
        self.contacts = {}

        if os.path.exists(filename):
            self.loadContact()
        else:
            self.saveContact()
            self.loadContact()

    def loadContact(self):
        self.contacts = pickle.load(open(self.filename, "rb"))
        print("loaded from", self.filename)

    def saveContact(self):
        pickle.dump(self.contacts, open(self.filename, "wb" ))
        print("saved to", self.filename)

  
