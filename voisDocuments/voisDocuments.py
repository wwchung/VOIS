'''
Team VOIS
Won-Woo Chung, Grant Li, Daniel Wu, Akihiro Ota
EECS 498 Section 9

Documents feature backend
'''


import os, sys, subprocess, glob
from docx import Document
import time


#															BEGIN HELPER FUNCTIONS





#Creates a path to the given folder name, given that it lives on the desktop
def createPath(folder_name):

	current_dir = os.getcwd() #Get current working directory --> Since VOIS lives on Desktop, will be Desktop/vois
	sep = 'vois'
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
