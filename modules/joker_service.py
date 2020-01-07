import threading
import time
import random
import traceback
import requests
import vk
from xml.etree import ElementTree


class JokerService(threading.Thread):
	daemon = True

	min_sleep = 60 * 60 * 24
	max_sleep = 60 * 60 * 24 * 3

	def __init__(self):
		super().__init__()
		self.stop = False

	def run(self):
		print('start joker service')
		while True:
			time.sleep(random.randrange(self.min_sleep, self.max_sleep))
			if self.stop:
				break

			for chat_id, peer_id in vk.get_chats():
				try:
					message = self._get_joke()
					message += '\n\nФьюить ха!'
					print('joker', chat_id, peer_id, message)
					vk.send_message(chat_id, message, [], peer_id)
				except:
					print(traceback.format_exc())

	def _get_joke(self):
		res = requests.get('http://rzhunemogu.ru/Rand.aspx?CType=%d' % random.choice([1, 11, 13, 18]))
		res_tree = ElementTree.fromstring(res.text)
		content = res_tree.find('content')
		if content is None:
			raise Exception('Content not found')
		return content.text
