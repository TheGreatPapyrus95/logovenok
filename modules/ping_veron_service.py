import json
import threading
import time
import random
import traceback
import vk


class VeronPinger(threading.Thread):
	daemon = True

	min_sleep = 60 * 60 * 24
	max_sleep = 60 * 60 * 24 * 7

	def __init__(self):
		super().__init__()
		self.stop = False
		self._attachments = self._load_attachments()

	def run(self):
		print('start veron ping service')
		while True:
			time.sleep(random.randrange(self.min_sleep, self.max_sleep))
			if self.stop:
				break

			print('ping veron', vk.get_chats())
			for chat_id, peer_id in vk.get_chats():
				try:
					file = random.choice(self._attachments)
					vk.send_message(chat_id, '@kiririn_akin, @matezius_tem, когда сходка?', [file], peer_id)
					time.sleep(1)
				except:
					print(traceback.format_exc())

	def _load_attachments(self):
		with open('./data/attachments_veron.json', encoding='utf-8') as f:
			return [vk.AttachmentFile(
				file['url'],
				file['type'],
				file['title']
			) for file in json.loads(f.read())]
