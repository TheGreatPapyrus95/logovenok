import re
import vk
import apiai
import json
import constants
from modules.reply_module import ReplyModule


class ReplyBtard(ReplyModule):
	token = 'bca51b4f8f1a4bfa9b0f532a19d5bc92'

	def reply(self, event):
		message = event.object.text.lower()

		if re.match(constants.appeal_regex, message):
			message = re.sub(constants.appeal_regex, '', message).strip()
			answer = self._generate_answer(message)
			vk.send_message(event.chat_id, answer)
			return True

		return False

	def _generate_answer(self, message):
		request = apiai.ApiAI(self.token).text_request()
		request.lang = 'ru'
		request.session_id = 'Logovenok'
		request.query = message
		response_json = json.loads(request.getresponse().read().decode('utf-8'))
		response = response_json['result']['fulfillment']['speech']
		return response or 'Я тибя нипанимаю!'
