#!/usr/bin/python
import pickle
import os

class ContactBook:

    def __init__(self, filename = "contacts.p"):
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

    def addContact(self, contactname, contact, contacttype = "phone"):
        assert contacttype == "phone" or contacttype == "email"

        if contactname not in self.contacts:
            self.contacts[contactname] = {"phone": None, "email": None}

        self.contacts[contactname][contacttype] = contact
        self.saveContact()

    def deleteContact(self, contactname):
        if contactname in self.contacts:
            self.contacts.pop(contactname, None)
            self.saveContact()

    def getContact(self, contactname, contacttype = "phone"):
        assert contacttype == "phone" or contacttype == "email"

        try: 
            retVal = self.contacts[contactname][contacttype]
            if retVal != None:
                return retVal
            else:
                print("No contact exists for", contactname)
        except KeyError:
            print("Error, couldn't find person")


    def listContacts(self):
        for k,v in self.contacts.items():
            print(k)
            print("\tPhone:", v['phone'])
            print("\tEmail:", v['email'])
            print()


c = ContactBook() 
c.listContacts()

#c.addContact("Dan", "1234567890")
#c.addContact("Dan", "yayayayay@gmail.com", "email")
#c.addContact("Aki", "foo@bar.com", "email")
#c.getContact("Aki", "email")
#print(c.getContact("Dan"))
#c.listContacts()


