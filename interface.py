'''
Team VOIS
Won-Woo Chung, Guangyu Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
import time
import vois_phone
import vois_email
import vois_documents
import vois_websearch


# Load kv file
Builder.load_file('interface.kv')

# Define home screen
class homeScreen(Screen):

    def quit(self):
        App.get_running_app().stop()

# Create screen manager
sm = ScreenManager()
sm.add_widget(homeScreen(name='home'))

# Add all phone screens
sm.add_widget(vois_phone.phoneHome(name='phoneHome'))
sm.add_widget(vois_phone.callScreen(name='call'))
sm.add_widget(vois_phone.textScreen(name='text'))

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
sm.add_widget(vois_websearch.SearchScreen(name='search'))
sm.add_widget(vois_websearch.ResultScreen(name='result'))

def execute(data):
    action_type = data['ActionType']
    context = data['Context']

    if action_type == 'Navigate':
        destination_screen = context['DestinationScreen']

        if destination_screen == 'Home':
            sm.current = 'home'
        elif destination_screen == 'Phone':
            sm.current = 'phoneHome'
        elif destination_screen == 'Email':
            sm.current = 'emailMain'
        elif destination_screen == 'Doc':
            sm.current = 'docs'
        elif destination_screen == 'Web':
            sm.current = 'search'
        else:
            print('Error: Invalid destination screen')

    elif action_type == 'PhoneCall':
        pass

    elif action_type == 'PhoneText':
        pass

    elif action_type == 'EmailCompose':
        pass

    elif action_type == 'EmailInbox':
        pass

    elif action_type == 'EmailSentMail':
        pass

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
        
        sm.current = 'search'
        time.sleep(0.5)
        sm.current = 'result'
        screen = vois_websearch.ResultScreen()
        screen.search(query)

    elif action_type == 'WebOpen':
        result_number = context['ResultNumber']

        if sm.current != 'result':
            print('Error: No search results')
            return

        screen = vois_websearch.ResultScreen()
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
        result_number = input('Enter result number: ')

        data['ActionType'] = 'WebOpen'
        data['Context'] = {
            'ResultNumber': result_number
        }

    else:
        print('Error: Invalid action type')
        return

    t = threading.Thread(target=execute, args=(data,))
    t.start()

def loop():
    while True:
        time.sleep(0.5)
        prompt()

class VOIS(App):

    def build(self):
        return sm

if __name__ == '__main__':
    t = threading.Thread(target=loop)
    t.start()
    VOIS().run()
