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
import documents as docs



# Create all possible screens. Use root.manager.current to control screens
Builder.load_string("""
<homeScreen>:
    GridLayout:
        cols: 1
        rows: 6

        Label:
            text: 'Welcome to VOIS'

        Button:
            text: 'Phone'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'phone'

        Button: 
            text: 'Email'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'email'

        Button:
            text: 'Documents'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'docs'

        Button: 
            text: 'Web Search'
            on_press: 
                root.manager.transition.direction = 'left'
                root.manager.current = 'web'

        Button:
            text: 'Exit'
            on_press: root.manager.get_screen('home').quit()

<phoneScreen>:
    GridLayout:
        cols: 1
        rows: 3

        Label:
            text: 'VOIS - Phone'

        TextInput:
            text: 'Enter Number'
            multiline: False
            on_text_validate: root.manager.get_screen('phone').printForm(self.text)

        Button:
            text: 'Back'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'home'


<emailScreen>:
    GridLayout:
        cols: 2
        rows: 2

        Label:
            text: 'VOIS - Email'

        Button: 
            text: 'Inbox'

        Button: 
            text: 'Compose'

        Button:
            text: 'Back'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'home'

<docsScreen>:

    GridLayout:
        cols: 1
        rows: 3

        Label:
            text: 'VOIS - Documents'


        GridLayout:

            cols: 2
            rows: 1

            Button:
                text: 'New Document'
                on_press: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'newDocs'

            Button:
                text: 'Previous Documents'
                on_press: 
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'prevDocs'

        GridLayout:
            cols: 1
            rows: 1

            Button:
                text: 'Back'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'home'


        

<newDocsScreen>
    GridLayout:
        cols: 1
        rows: 4

        Label:
            text: 'VOIS - Documents - New Document'

        GridLayout:
            cols: 2
            rows: 1

            Label: 
                text: 'Folder Name'

            Label: 
                text: 'Document Name'

        GridLayout:
            cols: 2
            rows: 1

            TextInput: 
                id: new_folder_id
                multiline: False
                focus: True

            TextInput:
                id: new_doc_id
                multiline: False
                focus: True
                on_text_validate: 
                    root.manager.get_screen('newDocs').newDoc(root.manager.get_screen('newDocs').ids.new_folder_id.text,self.text)
                    

        GridLayout:
            cols: 1
            rows: 1

            Button:
                text: 'Back'
                on_press: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'docs'



<prevDocsScreen>
    GridLayout:
        cols: 1
        rows: 4

        Label:
            text: 'VOIS - Documents - Previous Documents'

        GridLayout:
            cols: 2
            rows: 1

            Label: 
                text: 'Top 10 Most Recently Modified'

            Label:
                text: 'Search Folder'

        GridLayout:
            cols: 2
            rows: 1

            Button:
                text: 'Top 10'
                on_press:
                    root.manager.get_screen('listDocs').topTen()
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'listDocs'

            TextInput:
                id: prev_folder_id
                multiline: False
                focus: True
                on_text_validate:
                    root.manager.get_screen('prevDocs').byFolder(self.text)
                    
        GridLayout:
            cols: 1
            rows: 1

            Button:
                text: 'Back'
                on_press:
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'docs'


<listDocsScreen>
    GridLayout:
        cols: 1
        rows: 12

        Label:
            id: title
            text: 'VOIS - Documents - Previous Documents - View'

        Button:
            id: doc_0
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_1
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_2
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_3
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_4
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_5
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_6
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_7
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_8
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            id: doc_9
            text: ''
            on_press:
                root.manager.get_screen('listDocs').openDoc(self.text)

        Button:
            text: 'Back'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'prevDocs'


        

<webScreen>:
    GridLayout:
        cols: 1
        rows: 3

        Label:
            text: 'VOIS - Web Search'

        TextInput:
            text: 'Enter Search'
            multiline: False

        Button: 
            text: 'Back'
            on_press: 
                root.manager.transition.direction = 'right'
                root.manager.current = 'home'
        
""")

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