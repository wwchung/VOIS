from bs4 import BeautifulSoup
from functools import partial
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
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


class SearchScreen(Screen):

	search_input = ObjectProperty(None)

	def im_feeling_lucky(self):
		search_url = google_url + self.search_input.text.replace(' ', '+')

		try:
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
			headers = {'User-Agent': user_agent}

			req = urllib.request.Request(search_url, headers = headers)
			with urllib.request.urlopen(req) as response:
				html = response.read()

			soup = BeautifulSoup(html, 'html.parser')
			for title in soup.find_all('h3', class_='r'):
				try:
					url = str(title).split('/url?q=')[1].split('&amp')[0]
					webbrowser.get(chrome_path).open(url)
					break
				except IndexError:
					pass

		except Exception as e:
			print(str(e))


class ResultScreen(Screen):

	button1 = ObjectProperty(None)
	button2 = ObjectProperty(None)
	button3 = ObjectProperty(None)
	button4 = ObjectProperty(None)
	button5 = ObjectProperty(None)

	def show_result(self):
		search_url = google_url + self.manager.get_screen('search').search_input.text.replace(' ', '+')

		try:
			user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
			headers = {'User-Agent': user_agent}

			req = urllib.request.Request(search_url, headers=headers)
			with urllib.request.urlopen(req) as response:
				html = response.read()

			results = []

			soup = BeautifulSoup(html, 'html.parser')
			for title in soup.find_all('h3', class_='r'):
				results.append({'title': '', 'url': '', 'snippet': ''})

				try:
					url = str(title).split('/url?q=')[1].split('&amp')[0]
					results[-1]['title'] = title.text
					results[-1]['url'] = url

				except IndexError:
					pass

			i = 0
			for snippet in soup.find_all('span', class_='st'):
				results[i]['snippet'] = snippet.text[:72] + '...'
				i += 1

		except Exception as e:
			print(str(e))

		i = 0
		for result in results:
			if result['title'] != '':
				if i == 1:
					self.button1.text = '1. ' + result['title'] + '\n' + result['url'] + '\n' + result['snippet']
					self.button1.bind(on_press=partial(self.open_url, result['url']))
				elif i == 2:
					self.button2.text = '2. ' + result['title'] + '\n' + result['url'] + '\n' + result['snippet']
					self.button2.bind(on_press=partial(self.open_url, result['url']))
				elif i == 3:
					self.button3.text = '3. ' + result['title'] + '\n' + result['url'] + '\n' + result['snippet']
					self.button3.bind(on_press=partial(self.open_url, result['url']))
				elif i == 4:
					self.button4.text = '4. ' + result['title'] + '\n' + result['url'] + '\n' + result['snippet']
					self.button4.bind(on_press=partial(self.open_url, result['url']))
				elif i == 5:
					self.button5.text = '5. ' + result['title'] + '\n' + result['url'] + '\n' + result['snippet']
					self.button5.bind(on_press=partial(self.open_url, result['url']))
				i += 1

	def open_url(self, url, object):
		webbrowser.get(chrome_path).open(url)

	def reset(self):
		self.button1.text = 'Loading...'
		self.button2.text = 'Loading...'
		self.button3.text = 'Loading...'
		self.button4.text = 'Loading...'
		self.button5.text = 'Loading...'

sm = ScreenManager()
sm.add_widget(SearchScreen(name='search'))
sm.add_widget(ResultScreen(name='result'))


class SearchApp(App):

    def build(self):
        return sm


if __name__ == '__main__':
    SearchApp().run()
