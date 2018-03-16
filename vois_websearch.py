from bs4 import BeautifulSoup
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import urllib.parse
import urllib.request
import webbrowser


# Google Search
GOOGLE_URL = 'http://www.google.com/search?q='


# MacOS
CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'


SLICE_LENGTH = 88
def slice(str):
    if str:
        return str[:SLICE_LENGTH] + "..." if len(str) > SLICE_LENGTH else str
    else:
        return ''


class WebScreen(Screen):
	pass


class ResultScreen(Screen):

	buttons = []
	results = []

	def search(self, query):
		self.results.clear()
		
		search_url = GOOGLE_URL + query.replace(' ', '+')
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
					url = slice(str(title).split('/url?q=')[1].split('&amp')[0])
					snippet = slice(result.find('span', class_='st').get_text().replace('\n', ''))
					self.results.append({'title': title.text, 'url': url, 'snippet': snippet})
				except IndexError:
					pass

		except Exception as e:
			print(str(e))

		for i in range(6):
			if i < len(self.results):
				self.buttons[i].text = '[b]' + str(i + 1) + '. ' + self.results[i]['title'] + '[/b]\n' + self.results[i]['url'] + '\n' + self.results[i]['snippet']
			else:
				self.buttons[i].text = ''

	def open_url(self, result_number):
		webbrowser.get(CHROME_PATH).open(self.results[int(result_number) - 1]['url'])

	def reset_buttons(self):
		self.remove_buttons()

		for i in range(6):
			btn = Button(text='', font_size='16sp', text_size=(720, None), markup=True)
			if len(self.results) == 0:
				btn.text = 'Loading...'
			else:
				if i < len(self.results):
					btn.text = '[b]' + str(i + 1) + '. ' + self.results[i]['title'] + '[/b]\n' + self.results[i]['url'] + '\n' + self.results[i]['snippet']
				else:
					btn.text = ''
			self.buttons.append(btn)
			self.ids.box.add_widget(btn)

	def remove_buttons(self):
		for btn in self.buttons:
			self.ids.box.remove_widget(btn)
		self.buttons.clear()
