import json
import threading
import datetime
import time
import random
import traceback
import vk


class ScheduleService(threading.Thread):
	daemon = True

	def __init__(self):
		super().__init__()
		self.stop = False
		self._schedule = self._load_schedule()

	def run(self):
		print('start schedule service')
		while True:
			time.sleep(10)
			if self.stop:
				break

			for event in self._schedule:
				trigger_time = time.mktime(datetime.datetime(*event.time).timetuple()) - time.timezone
				delta = abs(time.time() - trigger_time)
				if delta < 5:
					for chat_id, peer_id in vk.get_chats():
						try:
							file = random.choice(event.attachment)
							vk.send_message(chat_id, event.message, [file], peer_id)
						except:
							print(traceback.format_exc())

	def _load_schedule(self):
		with open('./data/schedule.json', encoding='utf-8') as f:
			return [
				Event(x) for x in json.loads(f.read())
			]


class Event:
	def __init__(self, description_object):
		self.time = description_object['time']
		self.message = description_object['message']
		self.attachment = [
			vk.AttachmentFile(
				x['url'],
				x['type'],
				x['title']
			) for x in description_object['attachment']
		]
