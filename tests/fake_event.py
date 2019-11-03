from vk_api.bot_longpoll import VkBotEventType, VkBotMessageEvent


class FakeEventObject:
	type = VkBotEventType.MESSAGE_NEW

	def __init__(self, text, from_id):
		self.text = text
		self.from_id = from_id


class FakeEvent(VkBotMessageEvent):
	chat_id = 100

	def __init__(self, text, from_id=100000):
		self.object = FakeEventObject(text, from_id)
