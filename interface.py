'''
Team VOIS
Won-Woo Chung, Grant Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9

GUI layout
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import os
from docx import Document

#Import our features


#Phone files
from voisDocuments import voisDocuments as docs





#Email files
from gmail.credential import get_credentials
from gmail.retrieve_email import GetInboxMessages
from gmail.retrieve_email import GetSentMessages
from gmail.retrieve_email import ModifyMessage
from gmail.send_email import CreateMessage
from gmail.send_email import SendMessage

import httplib2
from apiclient import discovery

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text.markup import MarkupLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import arrow
from copy import deepcopy
from functools import partial
from email.utils import parseaddr
from kivy.uix.scrollview import ScrollView


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
SERVICE = discovery.build('gmail', 'v1', http=http)

# Default the sender to be the authenticated user
results = SERVICE.users().getProfile(userId='me').execute()
SENDER = results.get('emailAddress', [])


MSG_INFO = {}



#Documents files







#Web files




from voisEmail.alpha import vois_email
#import documents as docs



# Create all possible screens. Use root.manager.current to control screens
Builder.load_file('interface.kv')

# Declare All Screens
class homeScreen(Screen):

    #Quits the app
    def quit(self):
        App.get_running_app().stop()

    pass

class phoneScreen(Screen):

    def printForm(self,value):
        print('You entered:', value)












class emailScreen(Screen):
    pass





class EmailMainScreen(Screen):
    pass




class ComposeScreen(Screen):
    back_screen = ''

    def go_back(self):
        self.manager.current = self.back_screen

    def clear_inputs(self):
        self.back_screen = 'emailMain'
        self.ids.to_id.text = ''
        self.ids.subject_id.text = ''
        self.ids.body_id.text = ''

    def format_msg(self, from_inbox_forward, instance=None):
        self.back_screen = 'message'
        self.manager.current = 'compose'
        self.ids.to_id.text = '' if from_inbox_forward else MSG_INFO['addr']
        self.ids.subject_id.text = 'Fw: '+ MSG_INFO['subject'] \
                                    if from_inbox_forward \
                                    else MSG_INFO['subject']
        self.ids.body_id.text = MSG_INFO['forward_body'] \
                                if from_inbox_forward \
                                else MSG_INFO['body']


    def send_email(self):
        recievers = self.ids.to_id.text
        subject = self.ids.subject_id.text
        body = self.ids.body_id.text
        if recievers and (subject or body):
            [x.strip() for x in recievers.split(';')]
            recievers = recievers.split(';')
            message = CreateMessage(SENDER, recievers, subject, body)
            if SendMessage(SERVICE, "me", message):
                self.manager.current = 'emailMain'
                self.manager.transition.direction = 'down'


def shrink_it(text, length):
    if text:
        return text[:length] + "..." if len(text) > length else text
    else:
        return ''

class InboxScreen(Screen):
    email_btns = set()
    loading_label = True

    def clear_emails(self):
        for btn in self.email_btns:
            self.ids.box_id.remove_widget(btn)
        self.email_btns.clear()

    def get_inbox_emails(self):
        self.clear_emails()
        messages = GetInboxMessages(SERVICE)
        if self.loading_label:
            self.loading_label = False
            self.ids.box_id.remove_widget(self.ids.loading_label1)
        for msg in messages:
            msg_id = msg.get('msg_id')
            inbox_sender = parseaddr(msg.get('from'))[0] \
                           if parseaddr(msg.get('from'))[0] \
                           else msg.get('from')
            sender = shrink_it(inbox_sender, 40)
            timestamp = msg.get('timestamp')
            human_time = arrow.get(timestamp).humanize()
            subject = shrink_it(msg.get('subject'), 60)
            snippet = shrink_it(msg.get('snippet'), 80)
            reply = msg.get('reply') if msg.get('reply') else None

            dispay_text = "[font=FZHTK][size=30]" + sender + "    - [/size]" + \
            "[size=28]   " + human_time + \
            "[/size]\n[size=40][b]" + subject + "[/b][/size]\n[size=30]" + \
            snippet + "[/size]"

            if 'UNREAD' in msg.get('labels'):
                dispay_text = '[size=40][b]*NEW*[/b][size=40] ' + dispay_text

            btn = Button(text=dispay_text, markup=True, halign='left')
            btn.bind(on_release=partial(self.manager.get_screen('message')\
                    .dispay_message, {'msg_id': msg_id,
                                      'from': msg.get('from'),
                                      'to': SENDER,
                                      'reply': reply if reply \
                                                     else msg.get('from'),
                                      'subject': msg.get('subject'),
                                      'body': msg.get('body'),
                                      'timestamp': \
                                      str(arrow.get(timestamp).format()),
                                      'labels': msg.get('labels')}, False))
            btn.bind(texture_size=btn.setter('size'))
            self.ids.box_id.add_widget(btn)
            self.email_btns.add(btn)


class SentBoxScreen(Screen):
    email_btns = set()
    loading_label = True

    def clear_emails(self):
        for btn in self.email_btns:
            self.ids.sent_box_id.remove_widget(btn)
        self.email_btns.clear()


    def get_sent_emails(self):
        self.clear_emails()
        messages = GetSentMessages(SERVICE)
        if self.loading_label:
            self.loading_label = False
            self.ids.sent_box_id.remove_widget(self.ids.loading_label2)

        for msg in messages:
            msg_id = msg.get('msg_id')
            reciever = parseaddr(msg.get('to'))[0] \
                           if parseaddr(msg.get('to'))[0] \
                           else msg.get('to')
            sender = shrink_it(reciever, 40)
            timestamp = msg.get('timestamp')
            human_time = arrow.get(timestamp).humanize()
            subject = shrink_it(msg.get('subject'), 60)
            snippet = shrink_it(msg.get('snippet'), 80)

            dispay_text = "[font=FZHTK][size=30]" + sender + "[/size]    - " + \
            "[size=28]   " + human_time + \
            "[/size]\n[size=40][b]" + subject + "[/b][/size]\n[size=30]" + \
            snippet + "[/size]"

            btn = Button(text=dispay_text, markup=True, halign='left')
            btn.bind(on_release=partial(self.manager.get_screen('message')\
                    .dispay_message, {'msg_id': msg_id,
                                      'from': SENDER,
                                      'to': msg.get('to'),
                                      'subject': msg.get('subject'),
                                      'timestamp': \
                                      str(arrow.get(timestamp).format()),
                                      'body': msg.get('body')}, True))
            btn.bind(texture_size=btn.setter('size'))
            self.ids.sent_box_id.add_widget(btn)
            self.email_btns.add(btn)


class MessageScreen(Screen):
    forward_from_msg_list_btn = None
    back_screen = ''

    def go_back(self):
        self.manager.current = self.back_screen

    def dispay_message(self, msg_info, from_sentemail=False, instance=None):
        if from_sentemail:
            self.back_screen = 'sentBox'
            self.ids.compose_btn.text = 'Forward'
            if self.forward_from_msg_list_btn:
                self.ids.compose_btn.size_hint_x = 0.7
                self.ids.message_btns.remove_widget(self.\
                                                    forward_from_msg_list_btn)
                self.forward_from_msg_list_btn = None
        else:
            self.back_screen = 'inbox'
            self.ids.compose_btn.text = 'Reply'
            if not self.forward_from_msg_list_btn:
                self.forward_from_msg_list_btn = Button(text='Forward',
                                                 markup=True, height=80,
                                                 size_hint=(0.35, None))
                self.ids.message_btns.add_widget(self.forward_from_msg_list_btn)
                self.ids.compose_btn.size_hint_x = 0.35
                self.forward_from_msg_list_btn.bind(on_release=\
                    partial(self.manager.get_screen('compose').format_msg,
                            True))
        self.manager.current = 'message'
        self.ids.address_view_id.text = msg_info['to'] if from_sentemail \
                                                       else msg_info['from']
        self.ids.subject_view_id.text = msg_info['subject']
        self.ids.body_view_id.text = msg_info['body']

        # mark the message as READ
        if not from_sentemail and 'UNREAD' in msg_info['labels']:
            ModifyMessage(SERVICE, msg_info['msg_id'], {"removeLabelIds":
                                                        ['UNREAD']})
        MSG_INFO.clear()
        forward_msg = '\n\n\n' + \
                      '---------- Forwarded message ----------\n' + \
                      ' From: ' + msg_info['from'] + '\n' + \
                      ' Date: ' + msg_info['timestamp'] + '\n' + \
                      ' Subject: ' + msg_info['subject'] + '\n' + \
                      ' To: ' + msg_info['to'] + ' \n\n' + \
                      msg_info['body']
        if from_sentemail:
            MSG_INFO['addr'] = ''
            MSG_INFO['subject'] = 'Fw: ' + msg_info['subject']
            MSG_INFO['body'] = forward_msg
        else:
            MSG_INFO['addr'] = parseaddr(msg_info['reply'])[1]
            MSG_INFO['subject'] = 'Re: ' + msg_info['subject']
            MSG_INFO['body'] = '\n\n\n' + \
            'On ' + msg_info['timestamp'] + \
            ' <' + parseaddr(msg_info['from'])[1] + '> wrote:\n' + \
            msg_info['body']
            MSG_INFO['forward_body'] = forward_msg
        self.ids.compose_btn.bind(on_release=partial(self.manager\
                                  .get_screen('compose').format_msg, False))
















#Document home Screen
class docsScreen(Screen):
    pass

#Previous documents menu Screen
class prevDocsScreen(Screen):

    def byFolder(self,folder_name):

        #Check to see if the folder exists first. If not, display that the folder doesn't exist
        if not docs.folderExists(folder_name):
            self.ids.prev_folder_id.text = 'Error: The Specified Folder Does Not Exist'
            return 
        else:
            self.ids.prev_folder_id.text = ''
            sm.get_screen('listDocs').byFolder(folder_name)
            sm.transition.direction = 'left'
            sm.current = 'listDocs'

    pass

#Create new document Screen
class newDocsScreen(Screen):

    #Clears the folder and document text input
    def clearInput(self):
        self.ids.new_folder_id.text = ''
        self.ids.new_doc_id.text = ''

    #Will create a new document within the specified folder
    def newDoc(self,folder_name, doc_name):

        if docs.fileExists(folder_name,doc_name):
            self.ids.new_doc_id.text = 'Error: File Already Exists'
            return 

        
        docs.newDoc(folder_name,doc_name)
        self.clearInput()

        sm.transition.direction = 'right'
        sm.current = 'docs'
        
    pass

#Screen where previous documents show up
class listDocsScreen(Screen):

    data = {} #Maps files to their full path. Useful because don't want to display full path to user, but need it to open file
    # (ex: Essay.docx) maps to (ex: Desktop/folder1/Essay.docx)

    #Sets all Button text to empty
    def clearButtons(self):

        for i in range(10):
            doc_id = 'doc_' + str(i)
            self.ids[doc_id].text = ''

    #Given a full path, will find the file that it corresponds to using the self.data map
    def findDoc(self,target_path):
        for doc,path in self.data.items():
            if path == target_path:
                return doc

    #Populates button text with file names
    def setButtonText(self,paths):

        #Only show the first 10 results
        if len(paths) > 10:
            for i in range(10):
                doc_id = 'doc_' + str(i)

                self.ids[doc_id].text = self.findDoc(paths[i])

        else:
            for i in range(len(paths)):
                doc_id = 'doc_' + str(i)
                self.ids[doc_id].text = self.findDoc(paths[i])



    #Gets all word documents within a specific folder and displays them to the screen
    def byFolder(self,folder_name):

        self.clearButtons() #Clear previous Button text

        #Set title
        if folder_name != '':
            self.ids.title.text = 'VOIS - Documents - Previous Documents - ' + folder_name
        else:
            self.ids.title.text = 'VOIS - Documents - Previous Documents - Desktop'

        paths,self.data = docs.searchDirectory(folder_name)

        self.setButtonText(paths)

    #Gets top ten most recently modified documents and displays them to the screen
    def topTen(self):

        self.clearButtons() #Clear previous Button text
        self.ids.title.text = 'VOIS - Documents - Previous Documents - Top 10' #Set title

        paths,self.data = docs.topTenPrevDocs()

        self.setButtonText(paths)



    #Uses documents code to open a file with the given document name. Switches screen to prevDocs Screen if clikcs on valid button.
    def openDoc(self,doc_name):

        #If there is nothing to open, return without changing the screen.
        if doc_name == '':
            return

        #If this is a valid word document, open it
        if '.docx' in doc_name:

            sm.transition.direction = 'right'
            sm.current = 'prevDocs'

            file = self.data[doc_name]
            file = file.replace('.docx','',1) #Extract the docx off of the file 

            docs.openDoc(file) #Use the document name to retrieve the full path to the file and open it

    pass


class webScreen(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(homeScreen(name='home'))
sm.add_widget(phoneScreen(name='phone'))

#Add all email screens
sm.add_widget(emailScreen(name='email'))
sm.add_widget(vois_email.EmailMainScreen(name='emailMain'))
sm.add_widget(vois_email.ComposeScreen(name='compose'))
sm.add_widget(vois_email.InboxScreen(name='inbox'))
sm.add_widget(vois_email.MessageScreen(name='message'))
sm.add_widget(vois_email.SentBoxScreen(name='sentBox'))


#Add All documents Screens
sm.add_widget(docsScreen(name='docs'))
sm.add_widget(newDocsScreen(name='newDocs'))
sm.add_widget(prevDocsScreen(name='prevDocs'))
sm.add_widget(listDocsScreen(name='listDocs'))


sm.add_widget(webScreen(name='web'))


class vois(App):

    def build(self):
        return sm

if __name__ == '__main__':
    vois().run()