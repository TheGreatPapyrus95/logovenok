from vk_api.bot_longpoll import VkBotMessageEvent


class ReplyModule:
	def reply(self, event:VkBotMessageEvent) -> bool:
		return False
