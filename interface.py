'''
Team VOIS
Won-Woo Chung, Guangyu Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from threading import Thread
import time
import vois_phone
import vois_email
import vois_documents
import vois_websearch


# Load kv file
Builder.load_file('interface.kv')


# Define home screen
class HomeScreen(Screen):
    pass


# Define loading screen
class LoadingScreen(Screen):
    pass


# Create screen manager
sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(LoadingScreen(name='loading'))

# Add all phone screens
sm.add_widget(vois_phone.PhoneScreen(name='phone'))
sm.add_widget(vois_phone.CallScreen(name='call'))
sm.add_widget(vois_phone.TextScreen(name='text'))

# Add all email screens
sm.add_widget(vois_email.EmailMainScreen(name='emailMain'))
sm.add_widget(vois_email.ComposeScreen(name='compose'))
sm.add_widget(vois_email.InboxScreen(name='inbox'))
sm.add_widget(vois_email.MessageScreen(name='message'))
sm.add_widget(vois_email.SentBoxScreen(name='sentBox'))

# Add all document screens
sm.add_widget(vois_documents.docsScreen(name='docs'))
sm.add_widget(vois_documents.newDocsScreen(name='newDocs'))
sm.add_widget(vois_documents.prevDocsScreen(name='prevDocs'))
sm.add_widget(vois_documents.listDocsScreen(name='listDocs'))

# Add all web screens
sm.add_widget(vois_websearch.WebScreen(name='web'))
sm.add_widget(vois_websearch.ResultScreen(name='result'))


def execute(data):
    action_type = data['ActionType']
    context = data['Context']

    if action_type == 'Navigate':
        destination_screen = context['DestinationScreen']

        if destination_screen == 'Home':
            sm.current = 'home'
        elif destination_screen == 'Phone':
            sm.current = 'phone'
        elif destination_screen == 'Email':
            sm.current = 'emailMain'
        elif destination_screen == 'Doc':
            sm.current = 'docs'
        elif destination_screen == 'Web':
            sm.current = 'web'
        else:
            print('Error: Invalid destination screen')

    elif action_type == 'PhoneCall':
        destination_number = context['DestinationNumber']
        current_screen = sm.current

        sm.current = 'call'
        screen = vois_phone.CallScreen()
        screen.call(destination_number)
        time.sleep(1)
        sm.current = current_screen

    elif action_type == 'PhoneText':
        destination_number = context['DestinationNumber']
        message = context['Message']
        current_screen = sm.current

        sm.current = 'text'
        screen = vois_phone.TextScreen()
        screen.text(destination_number, message)
        time.sleep(1)
        sm.current = current_screen

    elif action_type == 'EmailCompose':
        pass

    elif action_type == 'EmailInbox':
        sm.current = 'inbox'

    elif action_type == 'EmailSentMail':
        sm.current = 'sentBox'

    elif action_type == 'DocumentCreate':
        pass

    elif action_type == 'DocumentSearch':
        pass

    elif action_type == 'DocumentTopTen':
        pass

    elif action_type == 'DocumentOpen':
        pass

    elif action_type == 'WebSearch':
        query = context['Query']

        if query == '':
            print('Error: Empty query')
            return
        
        sm.current = 'loading'
        time.sleep(0.5)
        sm.current = 'result'
        screen = vois_websearch.ResultScreen()
        screen.search(query)

    elif action_type == 'WebOpen':
        result_number = context['ResultNumber']

        screen = vois_websearch.ResultScreen()

        if int(result_number) > min(5, len(screen.results)):
            print('Error: Invalid result number')
            return

        screen.open_url(result_number)


def prompt():
    print()
    action_type = input('Enter action type: ')
    data = {
        'ActionType': '',
        'Context': {}
    }

    if action_type == 'Navigate':
        destionation_screen = input('Enter destination screen: ')
        
        data['ActionType'] = 'Navigate'
        data['Context'] = {
            'DestinationScreen': destionation_screen
        }

    elif action_type == 'PhoneCall':
        destination_number = input('Enter destination number: ')
        
        data['ActionType'] = 'PhoneCall'
        data['Context'] = {
            'DestinationNumber': destination_number
        }

    elif action_type == 'PhoneText':
        destination_number = input('Enter destination number: ')
        message = input('Enter message: ')

        data['ActionType'] = 'PhoneText'
        data['Context'] = {
            'DestinationNumber': destination_number,
            'Message': message
        }

    elif action_type == 'EmailCompose':
        to = input('Enter recipient: ')
        subject = input('Enter subject: ')
        message = input('Enter message: ')
        
        data['ActionType'] = 'EmailCompose'
        data['Context'] = {
            'To': to,
            'Subject': subject,
            'Message': message
        }
        
    elif action_type == 'EmailInbox':
        data['ActionType'] = 'EmailInbox'

    elif action_type == 'EmailSentMail':
        data['ActionType'] = 'EmailSentMail'

    elif action_type == 'DocumentCreate':
        file_name = input('Enter file name: ')
        folder_name = input('Enter folder name: ')
        
        data['ActionType'] = 'DocumentCreate'
        data['Context'] = {
            'FileName': file_name,
		    'FolderName': folder_name
        }

    elif action_type == 'DocumentSearch':
        folder_name = input('Enter folder name: ')
        
        data['ActionType'] = 'EmailCompose'
        data['Context'] = {
            'FolderName': folder_name
        }

    elif action_type == 'DocumentRecent':
        data['ActionType'] = 'DocumentRecent'

    elif action_type == 'DocumentOpen':
        document_number = input('Enter document number: ')
        
        data['ActionType'] = 'DocumentOpen'
        data['Context'] = {
		    'DocumentNumber': document_number
        }

    elif action_type == 'WebSearch':
        query = input('Enter query: ')

        data['ActionType'] = 'WebSearch'
        data['Context'] = {
            'Query': query
        }

    elif action_type == 'WebOpen':
        if sm.current != 'result':
            print('Error: Invalid action type')
            return

        result_number = input('Enter result number: ')

        data['ActionType'] = 'WebOpen'
        data['Context'] = {
            'ResultNumber': result_number
        }

    else:
        print('Error: Invalid action type')
        return

    execute(data)


def loop():
    while True:
        time.sleep(0.1)
        prompt()


class VOIS(App):

    def build(self):
        return sm


if __name__ == '__main__':
    t = Thread(target=loop)
    t.daemon = True     # Stop thread at shutdown
    t.start()
    VOIS().run()
