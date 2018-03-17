from email.utils import parseaddr
from gmail.credential import get_credentials
from gmail.retrieve_email import GetInboxMessages
from gmail.retrieve_email import GetSentMessages
from gmail.retrieve_email import ModifyMessage
from gmail.send_email import CreateMessage
from gmail.send_email import SendMessage
from googleapiclient import discovery
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
import arrow
import httplib2
import re
import time

# from gmail.credential import get_credentials
# from gmail.retrieve_email import GetInboxMessages
# from gmail.retrieve_email import GetSentMessages
# from gmail.retrieve_email import ModifyMessage
# from gmail.send_email import CreateMessage
# from gmail.send_email import SendMessage

# import httplib2
# from googleapiclient.discovery import build

# import kivy
# kivy.require('1.0.6') # replace with your current kivy version !

# from kivy.app import App
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.popup import Popup
# from kivy.core.text.markup import MarkupLabel
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.lang import Builder
# import arrow
# from copy import deepcopy
# from functools import partial
# from email.utils import parseaddr
# from kivy.uix.scrollview import ScrollView


CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2.Http())
SERVICE = discovery.build('gmail', 'v1', http=HTTP)
results = SERVICE.users().getProfile(userId='me').execute()
SENDER = results.get('emailAddress', [])

# SERVICE = None
# try:
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     SERVICE = build('gmail', 'v1', http=http)

#     # Default the sender to be the authenticated user
#     results = SERVICE.users().getProfile(userId='me').execute()
#     SENDER = results.get('emailAddress', [])
# except Exception as error:
#     SERVICE = None
#     print ("Error has occured: ", str(error))


# # Builder.load_file('VOISemail.kv')
# def check_internet():
#     if SERVICE is None:
#         ti = TextInput(text="Please check your Internet and restart VOIS",
#                        size_hint=(None, None), size=(300, 300))
#         pop = Popup(title='Error', content=ti,
#                     size_hint=(None, None), size=(400, 400))
#         pop.open()


SLICE_LENGTH = 88
def slice(str):
    if str:
        return str[:SLICE_LENGTH] + "..." if len(str) > SLICE_LENGTH else str
    else:
        return ''


# def shrink_it(text, length):
#     if text:
#         return text[:length] + "..." if len(text) > length else text
#     else:
#         return ''


class EmailScreen(Screen):
    pass


inbox_messages = []


class InboxScreen(Screen):

    buttons = []

    def get_inbox_emails(self):
        global inbox_messages
        inbox_messages.clear()
        inbox_messages = GetInboxMessages(SERVICE)

        for i in range(6):
            if i < len(inbox_messages):
                msg = inbox_messages[i]
                sender = parseaddr(msg.get('from'))[0] if parseaddr(msg.get('from'))[0] else msg.get('from')
                sent = arrow.get(msg.get('timestamp')).humanize()
                subject = slice(msg.get('subject'))
                snippet = slice(msg.get('snippet'))

                if 'UNREAD' in msg.get('labels'):
                    self.buttons[i].text = '[b]' + str(i + 1) + '. ' + sender + '[/b] - ' + sent + '\n' + subject + '\n' + snippet
                else:
                    self.buttons[i].text = '[color=bdbdbd][b]' + str(i + 1) + '. ' + sender + '[/b] - ' + sent + '\n' + subject + '\n' + snippet + '[/color]'
            else:
                self.buttons[i].text = ''

    def reset_buttons(self):
        self.remove_buttons()
        
        for i in range(6):
            btn = Button(text='', font_size='16sp', text_size=(1440, None), markup=True)
            if len(inbox_messages) == 0:
                btn.text = 'Loading...'
            else:
                if i < len(inbox_messages):
                    msg = inbox_messages[i]
                    sender = parseaddr(msg.get('from'))[0] if parseaddr(msg.get('from'))[0] else msg.get('from')
                    sent = arrow.get(msg.get('timestamp')).humanize()
                    subject = slice(msg.get('subject'))
                    snippet = slice(msg.get('snippet'))

                    if 'UNREAD' in msg.get('labels'):
                        btn.text = '[b]' + str(i + 1) + '. ' + sender + '[/b] - ' + sent + '\n' + subject + '\n' + snippet
                    else:
                        btn.text = '[color=bdbdbd][b]' + str(i + 1) + '. ' + sender + '[/b] - ' + sent + '\n' + subject + '\n' + snippet + '[/color]'
                else:
                    btn.text = ''
            self.buttons.append(btn)
            self.ids.box.add_widget(btn)

    def remove_buttons(self):
        for btn in self.buttons:
            self.ids.box.remove_widget(btn)
        self.buttons.clear()


sent_messages = []


class SentScreen(Screen):
    
    buttons = []

    def get_sent_emails(self):
        global sent_messages
        sent_messages.clear()
        sent_messages = GetSentMessages(SERVICE)
        
        for i in range(6):
            if i < len(sent_messages):
                msg = sent_messages[i]
                receiver = parseaddr(msg.get('to'))[0] if parseaddr(msg.get('to'))[0] else msg.get('to')
                sent = arrow.get(msg.get('timestamp')).humanize()
                subject = slice(msg.get('subject'))
                snippet = slice(msg.get('snippet'))

                self.buttons[i].text = '[b]' + str(i + 1) + '. ' + receiver + '[/b] - ' + sent + '\n' + subject + '\n' + snippet
            else:
                self.buttons[i].text = ''

    def reset_buttons(self):
        self.remove_buttons()
        
        for i in range(6):
            btn = Button(text='', font_size='16sp', text_size=(1440, None), markup=True)
            if len(sent_messages) == 0:
                btn.text = 'Loading...'
            else:
                if i < len(sent_messages):
                    msg = sent_messages[i]
                    receiver = parseaddr(msg.get('to'))[0] if parseaddr(msg.get('to'))[0] else msg.get('to')
                    sent = arrow.get(msg.get('timestamp')).humanize()
                    subject = slice(msg.get('subject'))
                    snippet = slice(msg.get('snippet'))

                    btn.text = '[b]' + str(i + 1) + '. ' + receiver + '[/b] - ' + sent + '\n' + subject + '\n' + snippet
                else:
                    btn.text = ''
            self.buttons.append(btn)
            self.ids.box.add_widget(btn)

    def remove_buttons(self):
        for btn in self.buttons:
            self.ids.box.remove_widget(btn)
        self.buttons.clear()


reply_msg = {}
forward_msg = {}

# MSG_INFO = {}


class MessageScreen(Screen):

    header_widgets = []
    body_widgets = []

    def open_message(self, msg, inbox):
        if inbox:
            self.header_widgets[1].text = msg['from']
        else:
            self.header_widgets[1].text = msg['to']
        self.header_widgets[3].text = msg['subject']
        time.sleep(0.5)
        self.body_widgets[0].text = ''
        try:
            self.body_widgets[0].text = msg['body']
        except Exception:
            self.body_widgets[0].text = "Failed to retrieve the email body, please view it on the web./n"

        if inbox:
            # mark message as READ
            if 'UNREAD' in msg['labels']:
                ModifyMessage(SERVICE, msg['msg_id'], {"removeLabelIds":['UNREAD']})

            reply_msg.clear()
            reply_msg['to'] = parseaddr(msg['from'])[1]
            reply_msg['subject'] = 'Re: ' + msg['subject']
            reply_msg['body'] = '\n\n\nOn ' + str(msg['timestamp']) + ' <' + parseaddr(msg['from'])[1] + '> wrote:\n' + msg['body']

            self.body_widgets[1].text = 'Reply'
        else:
            forward_msg.clear()
            forward_msg['addr'] = ''
            forward_msg['subject'] = 'Fw: ' + msg['subject']
            forward_msg['body'] = '\n\n\n' + '---------- Forwarded message ----------\n' + \
                ' From: ' + SENDER + '\n' + \
                ' Date: ' + str(msg['timestamp']) + '\n' + \
                ' Subject: ' + msg['subject'] + '\n' + \
                ' To: ' + msg['to'] + ' \n\n' + msg['body']
            self.body_widgets[1].text = 'Close'

    def reset_widgets(self):
        self.remove_widgets()

        from_label = Label(text='From:', font_size='20sp', size_hint=(0.2, None), height=120)
        self.header_widgets.append(from_label)
        self.ids.header_grid.add_widget(from_label)

        from_label = Label(text='', font_size='20sp', valign='center', size_hint=(0.8, None), height=120)
        self.header_widgets.append(from_label)
        self.ids.header_grid.add_widget(from_label)

        subject_label = Label(text='Subject:', font_size='20sp', size_hint=(0.2, None), height=120)
        self.header_widgets.append(subject_label)
        self.ids.header_grid.add_widget(subject_label)
        
        subject_label = Label(text='', font_size='20sp', valign='center', size_hint=(0.8, None), height=120)
        self.header_widgets.append(subject_label)
        self.ids.header_grid.add_widget(subject_label)
        
        body_text_input = TextInput(text='')
        self.body_widgets.append(body_text_input)
        self.ids.body_grid.add_widget(body_text_input)

        btn = Button(text='Reply', font_size='20sp', size_hint=(1, None), height=120)
        self.body_widgets.append(btn)
        self.ids.body_grid.add_widget(btn)

    def remove_widgets(self):
        for widget in self.header_widgets:
            self.ids.header_grid.remove_widget(widget)
        for widget in self.body_widgets:
            self.ids.body_grid.remove_widget(widget)
        self.header_widgets.clear()
        self.body_widgets.clear()


# class ComposeScreen(Screen):
#     back_screen = ''

#     def go_back(self):
#         self.manager.current = self.back_screen

#     def clear_inputs(self):
#         self.back_screen = 'emailMain'
#         self.ids.to_id.text = ''
#         self.ids.subject_id.text = ''
#         self.ids.body_id.text = ''

#     def format_msg(self, from_inbox_forward, instance=None):
#         self.back_screen = 'message'
#         self.manager.current = 'compose'
#         self.ids.to_id.text = '' if from_inbox_forward else MSG_INFO['addr']
#         self.ids.subject_id.text = 'Fw: '+ MSG_INFO['subject'] \
#                                     if from_inbox_forward \
#                                     else MSG_INFO['subject']
#         self.ids.body_id.text = MSG_INFO['forward_body'] \
#                                 if from_inbox_forward \
#                                 else MSG_INFO['body']


#     def send_email(self):
        check_internet()
        recievers = self.ids.to_id.text
        subject = self.ids.subject_id.text
        body = self.ids.body_id.text
        if recievers and (subject or body):
            [x.strip() for x in recievers.split(';')]
            recievers = recievers.split(';')
            message = CreateMessage(SENDER, recievers, subject, body)
            success, message = SendMessage(SERVICE, "me", message)
            if success:
                self.manager.current = 'emailMain'
                self.manager.transition.direction = 'down'
            else:
                ti = TextInput(text=message, size_hint=(None, None),
                           size=(300, 300))
                pop = Popup(title='Error', content=ti,
                            size_hint=(None, None), size=(400, 400))
                pop.open()


# NOT FULLY FUNCTIONAL COMPOSE SCREEN


# <ComposeScreen>:
#     on_pre_enter: root.reset_widgets()
#     GridLayout:
#         id: body_grid
#         cols: 1
#         GridLayout:
#             id: header_grid
#             cols: 2
#             size_hint: (1, None)
#             height: 120


class ComposeScreen(Screen):
    
    header_widgets = []
    body_widgets = []

    def compose_email(self, to, subject, body):
        self.header_widgets[1].text = to
        self.header_widgets[3].text = subject
        self.body_widgets[0].text = body

    def send_email(self):
        recievers = self.header_widgets[1].text
        subject = self.header_widgets[3].text
        body = self.body_widgets[0].text
        if recievers and (subject or body):
            [x.strip() for x in recievers.split(';')]
            recievers = recievers.split(';')
            message = CreateMessage(SENDER, recievers, subject, body)
            success, message = SendMessage(SERVICE, "me", message)
            if not success:
                ti = TextInput(text=message, size_hint=(None, None),
                           size=(300, 300))
                pop = Popup(title='Error', content=ti,
                            size_hint=(None, None), size=(400, 400))
                pop.open()

    def reset_widgets(self):
        self.remove_widgets()

        to_label = Label(text='To:', size_hint=(0.2, None), height=60)
        self.header_widgets.append(to_label)
        self.ids.header_grid.add_widget(to_label)

        to_text_input = TextInput(text='', size_hint=(0.8, None), height=60)
        self.header_widgets.append(to_text_input)
        self.ids.header_grid.add_widget(to_text_input)

        subject_label = Label(text='Subject:', size_hint=(0.2, None), height=60)
        self.header_widgets.append(subject_label)
        self.ids.header_grid.add_widget(subject_label)
        
        subject_text_input = TextInput(text='', size_hint=(0.8, None), height=60)
        self.header_widgets.append(subject_text_input)
        self.ids.header_grid.add_widget(subject_text_input)
        
        body_text_input = TextInput(text='')
        self.body_widgets.append(body_text_input)
        self.ids.body_grid.add_widget(body_text_input)

        btn = Button(text='Say \"send message\"', font_size='20sp', size_hint=(1, None), height=60)
        self.body_widgets.append(btn)
        self.ids.body_grid.add_widget(btn)

    def remove_widgets(self):
        for widget in self.header_widgets:
            self.ids.header_grid.remove_widget(widget)
        for widget in self.body_widgets:
            self.ids.body_grid.remove_widget(widget)
        self.header_widgets.clear()
        self.body_widgets.clear()
