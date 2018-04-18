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
from copy import deepcopy
import arrow
import httplib2
import re
import time


CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2.Http())
SERVICE = discovery.build('gmail', 'v1', http=HTTP)
results = SERVICE.users().getProfile(userId='me').execute()
SENDER = results.get('emailAddress', [])


SLICE_LENGTH = 88
def slice(str):
    if str:
        return str[:SLICE_LENGTH] + "..." if len(str) > SLICE_LENGTH else str
    else:
        return ''


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


global reply_msg
reply_msg = {}
global forward_msg
forward_msg = {}


class MessageScreen(Screen):

    header_widgets = []
    body_widgets = []

    def open_message(self, msg, inbox):
        if inbox:
            self.ids.message_from_to_label.text = u'From:'
            self.ids.message_from_to.text = msg['from']
            reply_to = msg.get('reply') if msg.get('reply') else (parseaddr(msg.get('from'))[1] if len(parseaddr(msg.get('from'))) > 1 else msg.get('from'))
            forward_from = msg['from']
        else:
            self.ids.message_from_to_label.text = u'To:'
            self.ids.message_from_to.text = msg['to']
            reply_to = parseaddr(msg.get('to'))[1] if len(parseaddr(msg.get('to'))) > 1 else msg.get('to')
            forward_from = SENDER
        
        self.ids.message_subject.text = msg['subject']
        time.sleep(0.25)
        self.ids.message_body.text = msg['body']

        if inbox:
            # mark message as READ
            if 'UNREAD' in msg['labels']:
                ModifyMessage(SERVICE, msg['msg_id'], {"removeLabelIds":['UNREAD']})
        reply_msg['to'] = reply_to
        reply_msg['subject'] = 'Re: ' + deepcopy(msg['subject'])
        reply_msg['body'] = u'\n\nOn ' + str(arrow.get(msg['timestamp']).format())[:-6] + u' \"' + reply_to + u'\" wrote:\n' + str(msg['body'])
        forward_msg.clear()
        forward_msg['to'] = ''
        forward_msg['subject'] = 'Fw: ' + deepcopy(msg['subject'])
        forward_msg['body'] = u'\n\n' + '---------- Forwarded message ----------\n' + \
            ' From: ' + forward_from + u'\n' + \
            ' Date: ' + str(arrow.get(msg['timestamp']).format())[:-6] + u'\n' + \
            ' Subject: ' + msg['subject'] + u'\n' + \
            ' To: ' + reply_to + u' \n\n' + str(msg['body'])
        # self.body_widgets[1].text = u'\"Reply with message {message}\" OR\n\"Forward to {to} with message {message}\"'


    # def reset_widgets(self):
    #     self.remove_widgets()

    #     # from_label = Label(text='From:', font_size='20sp', size_hint=(0.2, None), height=120)
    #     # self.header_widgets.append(from_label)
    #     # self.ids.header_grid.add_widget(from_label)

    #     # from_label = Label(text='', font_size='20sp', valign='center', size_hint=(0.8, None), height=120)
    #     # self.header_widgets.append(from_label)
    #     # self.ids.header_grid.add_widget(from_label)

    #     # subject_label = Label(text='Subject:', font_size='20sp', size_hint=(0.2, None), height=120)
    #     # self.header_widgets.append(subject_label)
    #     # self.ids.header_grid.add_widget(subject_label)
        
    #     # subject_label = Label(text='', font_size='20sp', valign='center', size_hint=(0.8, None), height=120)
    #     # self.header_widgets.append(subject_label)
    #     # self.ids.header_grid.add_widget(subject_label)
        
    #     # body_text_input = TextInput(text='', font_size='20sp', multiline=True, focus=True)
    #     # self.body_widgets.append(body_text_input)
    #     # self.ids.body_grid.add_widget(body_text_input)

    #     # btn = Button(text='Reply', font_size='20sp', size_hint=(1, None), height=120)
    #     # self.body_widgets.append(btn)
    #     # self.ids.body_grid.add_widget(btn)

    # def remove_widgets(self):
    #     for widget in self.header_widgets:
    #         self.ids.header_grid.remove_widget(widget)
    #     for widget in self.body_widgets:
    #         self.ids.body_grid.remove_widget(widget)
    #     self.header_widgets.clear()
    #     self.body_widgets.clear()

global message_sending
message_sending = {}

class ComposeScreen(Screen):
    header_widgets = []
    body_widgets = []

    def compose_email(self, to, subject, body, method='COMPOSE'):
        self.ids.message_to.text = ''
        self.ids.message_subject.text = ''
        self.ids.message_body.text = ''
        self.ids.message_to.text = to
        self.ids.message_subject.text = subject
        if method == 'REPLY':
            message_sending['body'] = deepcopy(body) + reply_msg['body']
            body += '\n\n---------- VOIS ----------\nPrevious message history will be included.'
        elif method == 'FORWARD':
            message_sending['body'] = deepcopy(body) + forward_msg['body']
            body += '\n\n---------- VOIS ----------\nPrevious message history will be included.'
        else:
            message_sending['body'] = deepcopy(body)
        try:
            self.ids.message_body.text = body
            # self.body_widgets[0].text = body
        except Exception:
            self.ids.message_body.text = "Message attached. Use voice command to send."
            # self.body_widgets[0].text = "Message attached. Use voice command to send."
        
    def send_email(self):
        recievers = self.ids.message_to.text
        subject = self.ids.message_subject.text
        if recievers and (subject or message_sending['body']):
            [x.strip() for x in recievers.split(';')]
            recievers = recievers.split(';')
            message = CreateMessage(SENDER, recievers, subject, message_sending['body'])
            success, message = SendMessage(SERVICE, "me", message)
            if not success:
                ti = TextInput(text=message, size_hint=(None, None),
                           size=(300, 300))
                pop = Popup(title='Error', content=ti,
                            size_hint=(None, None), size=(400, 400))
                pop.open()
                time.sleep(3)
                pop.dismiss()

    # def reset_widgets(self):
    #     # self.remove_widgets()
    #     self.ids.message_to.text = ''
    #     self.ids.message_subject.text = ''
    #     self.ids.message_body.text = ''
    #     # to_label = Label(text='To:', font_size='20sp', size_hint=(0.2, None), height=120)
    #     # self.header_widgets.append(to_label)
    #     # self.ids.header_grid.add_widget(to_label)

    #     # to_text_input = TextInput(text='', font_size='20sp', size_hint=(0.8, None), height=120)
    #     # self.header_widgets.append(to_text_input)
    #     # self.ids.header_grid.add_widget(to_text_input)

    #     # subject_label = Label(text='Subject:', font_size='20sp', size_hint=(0.2, None), height=120)
    #     # self.header_widgets.append(subject_label)
    #     # self.ids.header_grid.add_widget(subject_label)
        
    #     # subject_text_input = TextInput(text='', font_size='20sp', size_hint=(0.8, None), height=120)
    #     # self.header_widgets.append(subject_text_input)
    #     # self.ids.header_grid.add_widget(subject_text_input)
        
    #     # body_text_input = TextInput(text='', font_size='20sp')
    #     # self.body_widgets.append(body_text_input)
    #     # self.ids.body_grid.add_widget(body_text_input)

    #     # btn = Button(text='\"Send email\"', font_size='20sp', size_hint=(1, None), height=120)
    #     # self.body_widgets.append(btn)
    #     # self.ids.body_grid.add_widget(btn)

    # def remove_widgets(self):
    #     for widget in self.header_widgets:
    #         self.ids.header_grid.remove_widget(widget)
    #     for widget in self.body_widgets:
    #         self.ids.body_grid.remove_widget(widget)
    #     self.header_widgets.clear()
    #     self.body_widgets.clear()
