import re
import time
import mechanize
from urllib import parse
from bs4 import BeautifulSoup
import constants
import vk
from modules.reply_module import ReplyModule


class ReplyJosephCorrection(ReplyModule):
	search_base_url = 'https://www.google.com/search'
	min_interval = 60

	def __init__(self):
		self._last_reply_time = 0

	def reply(self, event):
		if event.object.from_id == constants.joseph_id \
			and time.time() - self._last_reply_time > self.min_interval \
			:
			message = event.object.text.lower()
			message = re.sub(constants.appeal_regex, '', message).strip()

			if 3 <= len(message) <= 70:
				correction = self._get_correction(message)
				if correction:
					answer = 'Пьянь, ты имел в виду "%s"?' % correction
					vk.send_message(event.chat_id, answer)
					self._last_reply_time = time.time()
					return True

		return False

	def _get_correction(self, text):
		url = self.search_base_url + '?' + parse.urlencode({
			'q': text,
			'hl': 'en',
			'lr': 'lang_ru',
			'ie': 'UTF-8',
			'oe': 'UTF-8',
		})
		headers = [
			('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'),
			('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
			('Accept-Language', 'en-US,en;q=0.5'),
			('Accept-Encoding', 'gzip, deflate'),
			('DNT', '1'),
			('Connection', 'keep-alive'),
			('Upgrade-Insecure-Requests', '1'),
		]
		chrome = mechanize.Browser()
		chrome.set_handle_robots(False)
		chrome.addheaders = headers

		res = chrome.open(url)
		html = res.read().decode(encoding='utf-8')
		if res.code == 200:
			soup = BeautifulSoup(html, features='html.parser')
			node = soup.select_one('div#taw')
			node_text = node.get_text().lower()
			if node_text.startswith('did you mean:'):
				return node.select_one('a').get_text().strip()
			if node_text.startswith('showing results for'):
				return node.select_one('a').get_text().strip()

		print('correction status:', res.code)
		print(html)

		return None
