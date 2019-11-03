import os
import vk


class TestVk:
	def setup(self):
		vk._chats_file_path = './tests/chats.dat'
		vk._chats.clear()

	def teardown(self):
		os.remove(vk._chats_file_path)

	def test_remember(self):
		vk.load_chats_list()

		vk.remember_chat(1, 3)
		assert(vk.get_chats() == {(1, 3)})

		vk.remember_chat(3, 5)
		assert(vk.get_chats() == {(1, 3), (3, 5)})

		vk.remember_chat(1, 3)
		assert(vk.get_chats() == {(1, 3), (3, 5)})

		with open(vk._chats_file_path) as f:
			assert(f.readlines() == ['1 3\n', '3 5\n'])

	def test_load_remembered_chats(self):
		with open(vk._chats_file_path, mode='w') as f:
			f.write('1 3\n3 5\n2 4\n')

		vk.load_chats_list()
		assert(vk.get_chats() == {(1, 3), (3, 5), (2, 4)})
