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
        print(self.filename)
        self.contacts = pickle.load(open(self.filename, "rb"))
        print("loaded from", self.filename)

    def saveContact(self):
        pickle.dump(self.contacts, open(self.filename, "wb" ))
        print("saved to", self.filename)

    def addContact(self, contactname, contact, contacttype = "phone"):
        contactname = contactname.lower()
        assert contacttype == "phone" or contacttype == "email"

        if contactname not in self.contacts:
            self.contacts[contactname] = {"phone": None, "email": None}

        self.contacts[contactname][contacttype] = contact
        self.saveContact()

    def deleteContact(self, contactname):
        contactname = contactname.lower()
        if contactname in self.contacts:
            self.contacts.pop(contactname, None)
            self.saveContact()

    def getContact(self, contactname, contacttype = "phone"):
        contactname = contactname.lower()
        assert contacttype == "phone" or contacttype == "email"

        try: 
            retVal = self.contacts[contactname][contacttype]
            if retVal != None:
                return retVal
            else:
                print("No contact exists for", contactname)
                return None
        except KeyError:
            print("Error: couldn't find person")
            return None
            
    def clearContacts(self):
        self.contacts = {}
        self.saveContact()


    def listContacts(self):
        for k,v in self.contacts.items():
            print(k)
            print("\tPhone:", v['phone'])
            print("\tEmail:", v['email'])
            print()


c = ContactBook("contacts.p") 

c.clearContacts()

c.addContact("Dan", "7347806855")
c.addContact("Dan", "dwuu@umich.edu", "email")
c.addContact("Grant", "7818988832")
c.addContact("Grant", "guangyu@umich.edu", "email")
c.addContact("Aki", "7345068603")
c.addContact("Aki", "guangyu@umich.edu", "email")
c.addContact("voice", "eecs498.vois@gmail.com", "email")
c.addContact("test", "eecs498.vois@gmail.com", "email")

c.listContacts()



  
