import os
import requests
import random
from typing import List
from vk_api import vk_api, VkUpload

token = '54db9714241ed308a860a986a7bbeff27e4218c09eca1fd2402e75aba2e352cb2539f643fd3003404e68c'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

_chats_file_path = './data/chats.dat'
_chats = set()


class AttachmentFile:
	def __init__(self, url, file_type, title=''):
		self.url = url
		self.type = file_type
		self.title = title


def send_message(chat_id, text, attach_files:List[AttachmentFile]=(), peer_id=None):
	attachments = [create_message_attachment(file, peer_id) for file in attach_files]

	vk.messages.send(
		random_id=round(random.random() * 10 ** 9),
		chat_id=chat_id,
		message=text,
		attachment=','.join(attachments)
	)

def create_message_attachment(attachment:AttachmentFile, peer_id=None):
	session = requests.Session()
	stream = session.get(attachment.url, stream=True)
	if attachment.type == 'photo':
		file = upload.photo_messages(photos=stream.raw)[0]
		return 'photo%d_%d' % (file['owner_id'], file['id'])
	elif attachment.type == 'doc':
		file = upload.document_message(doc=stream.raw, title=attachment.title, peer_id=peer_id)
		return 'doc%d_%d' % (file['doc']['owner_id'], file['doc']['id'])
	return None


def load_chats_list():
	global _chats

	if os.path.exists(_chats_file_path):
		with open(_chats_file_path, encoding='utf-8', mode='r') as f:
			lines = f.readlines()
		chats = set()
		for line in lines:
			chat_id, peer_id = line.strip().split(' ')
			chats.add((int(chat_id), int(peer_id)))

		_chats = chats

def remember_chat(chat_id, peer_id):
	_chats.add((chat_id, peer_id))

	with open(_chats_file_path, encoding='utf-8', mode='w') as f:
		f.writelines(['%d %d\n' % (chat_id, peer_id) for chat_id, peer_id in _chats])

def get_chats():
	return _chats
