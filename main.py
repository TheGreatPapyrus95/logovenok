from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import time
import traceback
import constants
import vk
from modules.reply_basic import ReplyBasic
from modules.reply_joseph import ReplyJoseph
from modules.reply_btard import ReplyBtard
from modules.ping_veron_service import VeronPinger
from modules.anime_hating_service import AnimeHatingService
from modules.event_service import EventService

def main():
	vk.load_chats_list()
	VeronPinger().start()
	AnimeHatingService().start()
	EventService().start()

	while True:
		try:
			longpoll = VkBotLongPoll(vk.vk_session, constants.group_id)
			print('listen for events ...')
			for event in longpoll.listen():
				handle_event(event)
		except KeyboardInterrupt:
			print('exit')
			exit(0)
		except:
			print(traceback.format_exc())

		time.sleep(1)


reply_modules = [
	ReplyBasic(),
	ReplyJoseph(),
	ReplyBtard(),
]

def handle_event(event):
	if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
		vk.remember_chat(event.chat_id, event.object.peer_id)

		for module in reply_modules:
			if module.reply(event):
				break


if __name__ == '__main__':
	main()
