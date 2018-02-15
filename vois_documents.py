'''
Team VOIS
Won-Woo Chung, Grant Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9

Documents feature backend
'''


import os, sys, subprocess, glob
from docx import Document
import time
from kivy.uix.screenmanager import ScreenManager, Screen


#															BEGIN HELPER FUNCTIONS





#Creates a path to the given folder name, given that it lives on the desktop
def createPath(folder_name):

	current_dir = os.getcwd() #Get current working directory --> Since VOIS lives on Desktop, will be Desktop/vois
	sep = 'VOIS'
	path = current_dir.split(sep,1)[0] #Remove vois from path. The path now is the Desktop

	#If we don't have an empty folder name, then we want to add it to the path
	if folder_name != '':
		path = path + folder_name + '/'

	return path

#Checks whether a folder exists. Returns true if it does, false otherwise
def folderExists(folder_name):

	path = createPath(folder_name)

	if not os.path.isdir(path):
		return False

	return True

#Checks whether a file already exists. Returns true if it does, false otherwise.
def fileExists(folder_name,doc_name):

	#If the folder doesn't exist, the file cannot exist within it
	if not folderExists(folder_name):
		return False

	#Construct the full path name of the file
	path = createPath(folder_name)
	new_file = path + doc_name

	#Check if it exists
	if os.path.isfile(new_file+'.docx'):
		return True

	return False

#Takes an array of word documents and sorts them based on the time they were last modified
def sortByModified(docs):
	docs.sort(key=lambda x: os.path.getmtime(x)) #Sort by date modified

	docs.reverse() #Reverse to get most recent item first

	#No need to return since these methods modify the list in place


#Opens a document given a document name
def openDoc(doc_name):
	subprocess.run(['open',doc_name + '.docx'])





#															END HELPER FUNCTIONS






#													BEGIN FUNCTIONS USED DIRECTLY BY VOIS





#Will create an open a new document within the specified folder with doc_name. Will save the document to the desktop if no folder name given
def newDoc(folder_name,doc_name):

	path = createPath(folder_name) #Get the path to save to

	#If this folder doesn't exist, then create a new folder
	if not folderExists(folder_name):
		os.makedirs(path)

	new_file = path + doc_name #Construct new file name

	#Now create the new document and save it to the constructed path
	new = Document()
	new.save(new_file + '.docx')
	openDoc(new_file) #Open it



'''
Get top 10 most recently modified from a specific folder. If none is specified, search the Desktop
Returns:
	a list of full paths to open files. Sorted by most recently modified (Ex: Desktop/folder1/Essay.docx)
	a dictionary mapping file names (ex: Essay.docx) to full paths (Ex: Desktop/folder1/Essay.docx)
'''
def searchDirectory(folder_name=''):
	documents_map = {} #Maps what the user sees to full paths so that the file can be opened
	full_paths = [] #Need this for sorting capabilities

	root = createPath(folder_name)

	#Only search through this specific folder
	for file in os.listdir(root):
		if file.endswith('.docx'):
			documents_map[file] = root + file
			full_paths.append(root+file)


	sortByModified(full_paths)

	return full_paths, documents_map



'''
Get top 10 most recently modified documents from Desktop (or subfolder) and return them.
Returns:
	a list of full paths to open files. Sorted by most recently modified (Ex: Desktop/folder1/Essay.docx)
	a dictionary mapping file names (ex: Essay.docx) to full paths (Ex: Desktop/folder1/Essay.docx)
'''
def topTenPrevDocs():
	documents_map = {} #Maps what the user sees to full paths so that the file can be opened
	full_paths = [] #Need this for sorting capabilities

	root = createPath('')

	#Search through Desktop and all of its subfolders
	for subdir,dirs,files in os.walk(root):
		for file in files:
			#Only add word documents that exist
			if '.docx' in file and not '~$' in file:

				#Format the file correctly
				if subdir != root:
					file = '/' + file

				path = subdir + file

				full_paths.append(str(path)) #This is the full path, stored behind the scenes so that it can be opened

				split = path.rsplit('/',1) #split on the last slash

				documents_map[split[1]] = path


	sortByModified(full_paths)

	return full_paths, documents_map






#												BEGIN CLASSES FOR SCREENS AND ASSOCIATED FUNCTIONS



#Document home Screen
class docsScreen(Screen):
    pass

#Previous documents menu Screen
class prevDocsScreen(Screen):
    
    #Clears text input
    def clearInput(self):
        self.ids.prev_folder_id.text = ''

    #Searches for word documents in a specific folder
    def byFolder(self,folder_name):

        #Check to see if the folder exists first. If not, display that the folder doesn't exist
        if not folderExists(folder_name):
            self.ids.prev_folder_id.text = 'Error: The Specified Folder Does Not Exist'
            return
        else:
            self.clearInput()
            self.manager.get_screen('listDocs').byFolder(folder_name)
            self.manager.transition.direction = 'left'
            self.manager.current = 'listDocs'


#Create new document Screen
class newDocsScreen(Screen):

    #Clears the folder and document text input
    def clearInput(self):
        self.ids.new_folder_id.text = ''
        self.ids.new_doc_id.text = ''

    #Will create a new document within the specified folder
    def newDoc(self,folder_name, doc_name):

        if fileExists(folder_name,doc_name):
            self.ids.new_doc_id.text = 'Error: File Already Exists'
            return


        newDoc(folder_name,doc_name)
        self.clearInput()

        self.manager.transition.direction = 'right'
        self.manager.current = 'docs'


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
                self.ids[doc_id].font_name = 'FZHTK'

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

        paths,self.data = searchDirectory(folder_name)

        self.setButtonText(paths)

    #Gets top ten most recently modified documents and displays them to the screen
    def topTen(self):

        self.clearButtons() #Clear previous Button text
        self.ids.title.text = 'VOIS - Documents - Previous Documents - Top 10' #Set title

        paths,self.data = topTenPrevDocs()

        self.setButtonText(paths)



    #Uses documents code to open a file with the given document name. Switches screen to prevDocs Screen if clikcs on valid button.
    def openDoc(self,doc_name):

        #If there is nothing to open, return without changing the screen.
        if doc_name == '':
            return

        #If this is a valid word document, open it
        if '.docx' in doc_name:

            self.manager.transition.direction = 'right'
            self.manager.current = 'prevDocs'

            file = self.data[doc_name]
            file = file.replace('.docx','',1) #Extract the docx off of the file

            openDoc(file) #Use the document name to retrieve the full path to the file and open it


