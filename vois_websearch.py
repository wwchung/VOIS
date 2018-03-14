from bs4 import BeautifulSoup
from functools import partial
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import urllib.parse
import urllib.request
import webbrowser

# Google Search
google_url = 'http://www.google.com/search?q='

# MacOS
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

# Windows
# chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'


class WebScreen(Screen):
	pass

	# def im_feeling_lucky(self, query):
	# 	search_url = google_url + query.replace(' ', '+')
	# 	try:
	# 		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	# 		headers = {'User-Agent': user_agent}

	# 		req = urllib.request.Request(search_url, headers = headers)
	# 		with urllib.request.urlopen(req) as response:
	# 			html = response.read()

	# 		soup = BeautifulSoup(html, 'html.parser')
	# 		for title in soup.find_all('h3', class_='r'):
	# 			try:
	# 				url = str(title).split('/url?q=')[1].split('&amp')[0]
	# 				webbrowser.get(chrome_path).open(url)
	# 				break
	# 			except IndexError:
	# 				pass
	# 	except Exception as e:
	# 		print(str(e))


class ResultScreen(Screen):

	buttons = []
	results = []

	def search(self, query):
		self.results.clear()
		
		search_url = google_url + query.replace(' ', '+')
		try:
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
			headers = {'User-Agent': user_agent}

			req = urllib.request.Request(search_url, headers=headers)
			with urllib.request.urlopen(req) as response:
				html = response.read()

			soup = BeautifulSoup(html, 'html.parser')
			for result in soup.find_all('div', class_='g'):
				try:
					title = result.find('h3', class_='r')
					url = str(title).split('/url?q=')[1].split('&amp')[0]
					if len(url) > 64:
						url = url[:64] + '...'
					snippet = result.find('span', class_='st').get_text()
					if len(snippet) > 64:
						snippet = snippet[:64] + '...'
					self.results.append({'title': title.text, 'url': url, 'snippet': snippet})
				except IndexError:
					pass

		except Exception as e:
			print(str(e))

		for i in range(5):
			if i < len(self.results):
				self.buttons[i].text = str(i + 1) + '. ' + self.results[i]['title'] + '\n' + self.results[i]['url'] + '\n' + self.results[i]['snippet']
			else:
				self.buttons[i].text = ''

	def open_url(self, index):
		webbrowser.get(chrome_path).open(self.results[int(index) - 1]['url'])

	def reset_buttons(self):
		self.remove_buttons()
		for i in range(5):
			btn = Button(text='', font_size='16sp')
			if len(self.results) == 0:
				btn.text = 'Loading...'
			else:
				if i < len(self.results):
					btn.text = str(i + 1) + '. ' + self.results[i]['title'] + '\n' + self.results[i]['url'] + '\n' + self.results[i]['snippet']
				else:
					btn.text = ''
			self.buttons.append(btn)
			self.ids.box.add_widget(btn)

	def remove_buttons(self):
		for btn in self.buttons:
			self.ids.box.remove_widget(btn)
		self.buttons.clear()
