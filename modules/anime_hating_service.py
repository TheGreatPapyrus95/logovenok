import json
import threading
import time
import random
import traceback
import vk


class AnimeHatingService(threading.Thread):
	daemon = True

	min_sleep = 60 * 60 * 24 * 3
	max_sleep = 60 * 60 * 24 * 21

	def __init__(self):
		super().__init__()
		self.stop = False
		self._quotes = self._load_quotes()
		self._attachments = self._load_attachments()

	def run(self):
		print('start anime hating service')
		while True:
			time.sleep(random.randrange(self.min_sleep, self.max_sleep))
			if self.stop:
				break

			print('anime', vk.get_chats())
			for chat_id, peer_id in vk.get_chats():
				try:
					file = random.choice(self._attachments)
					message = random.choice(self._quotes)
					vk.send_message(chat_id, message, [file], peer_id)
					time.sleep(1)
				except:
					print(traceback.format_exc())

	def _load_quotes(self):
		with open('./data/anime_quotes.json', encoding='utf-8') as f:
			return json.loads(f.read())

	def _load_attachments(self):
		with open('./data/attachments_anime.json', encoding='utf-8') as f:
			return [vk.AttachmentFile(
				file['url'],
				file['type'],
				file['title']
			) for file in json.loads(f.read())]
