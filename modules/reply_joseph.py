import json
import random
import time
import constants
import vk
from modules.reply_module import ReplyModule


class ReplyJoseph(ReplyModule):
	min_interval = 3600
	session_length = 180

	def __init__(self):
		self._quotes = self._load_quotes()
		self._last_reply_time = 0
		self._session_start_time = 0
		self._recent_messages = []

	def reply(self, event):
		if event.object.from_id == constants.joseph_id:
			quote = self._get_quote()

			if time.time() - self._last_reply_time > self.min_interval:
				self._send_message(event.chat_id, quote)
				self._last_reply_time = time.time()
				self._session_start_time = time.time()
				return True

			if time.time() - self._session_start_time < self.session_length:
				self._send_message(event.chat_id, quote)
				self._last_reply_time = time.time()
				return True

		return False

	def _send_message(self, chat_id, quote):
		vk.send_message(chat_id, quote)
		self._recent_messages.append(quote)
		if len(self._recent_messages) > 5:
			self._recent_messages.pop(0)

	def _get_quote(self):
		while True:
			quote = random.choice(self._quotes)
			if quote not in self._recent_messages:
				return quote

	def _load_quotes(self):
		with open('./data/joseph_quotes.json', encoding='utf-8') as f:
			return json.loads(f.read())
