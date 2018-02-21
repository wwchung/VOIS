'''
Team VOIS
Won-Woo Chung, Grant Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9

GUI layout
'''
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#Import our features
#Phone Features
import vois_phone

#Email files
import vois_email

#Document files
import vois_documents

#Web files
import vois_websearch


# Create all possible screens
Builder.load_file('interface.kv')

#Define home Screen
class homeScreen(Screen):
    #Quits the app
    def quit(self):
        App.get_running_app().stop()



# Create the screen manager
sm = ScreenManager()
sm.add_widget(homeScreen(name='home'))

#Add all phone screens
sm.add_widget(vois_phone.phoneHome(name='phoneHome'))
sm.add_widget(vois_phone.callScreen(name='call'))
sm.add_widget(vois_phone.textScreen(name='text'))

#Add all email screens
sm.add_widget(vois_email.EmailMainScreen(name='emailMain'))
sm.add_widget(vois_email.ComposeScreen(name='compose'))
sm.add_widget(vois_email.InboxScreen(name='inbox'))
sm.add_widget(vois_email.MessageScreen(name='message'))
sm.add_widget(vois_email.SentBoxScreen(name='sentBox'))


#Add All documents Screens
sm.add_widget(vois_documents.docsScreen(name='docs'))
sm.add_widget(vois_documents.newDocsScreen(name='newDocs'))
sm.add_widget(vois_documents.prevDocsScreen(name='prevDocs'))
sm.add_widget(vois_documents.listDocsScreen(name='listDocs'))

#Add all web search screens
sm.add_widget(vois_websearch.SearchScreen(name='search'))
sm.add_widget(vois_websearch.ResultScreen(name='result'))

class vois(App):

    def build(self):
        return sm

if __name__ == '__main__':
    vois().run()
