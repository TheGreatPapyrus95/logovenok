import json
import random
import re
import time
from typing import List
import constants
import vk
from modules.reply_module import ReplyModule


class Answer:
	def __init__(self, query, type, answers):
		self.query = query
		self.type = type
		self.answers = answers

	def __repr__(self):
		return '%s %s %s' % (self.query, self.answers, self.type)


class ReplyBasic(ReplyModule):
	often_min_interval = 10

	def __init__(self):
		self._answers = self._load_answers('./data/answers.json')
		self._answers_often = self._load_answers('./data/answers_often.json')
		self._last_often_reply_time = 0

	def reply(self, event):
		if self._reply_using_list(event, self._answers):
			return True

		if time.time() - self._last_often_reply_time > self.often_min_interval \
			and self._reply_using_list(event, self._answers_often) \
			:
			self._last_often_reply_time = time.time()
			return True

		return False

	def _reply_using_list(self, event, answers:List[Answer]):
		message = event.object.text.lower()
		message = re.sub(constants.appeal_regex, '', message).strip()

		for answer in answers:
			if self._match(answer, message):
				vk.send_message(event.chat_id, random.choice(answer.answers))
				return True

		return False

	def _match(self, answer, message):
		if answer.type == 'str' and message in answer.query:
			return True
		if answer.type == 'regex' and [True for regex in answer.query if re.fullmatch(regex, message)]:
			return True
		return False

	def _load_answers(self, file_path):
		with open(file_path, encoding='utf-8') as f:
			return [Answer(
				item['query'],
				item['type'],
				item['answers']
			) for item in json.loads(f.read())]
