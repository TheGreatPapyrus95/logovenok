import pytest
from unittest.mock import Mock
import vk
from modules.reply_basic import ReplyBasic
from tests.fake_event import FakeEvent


class TestReplyBasic:
	@pytest.fixture(autouse=True)
	def create_module(self):
		self.module = ReplyBasic()

	@pytest.fixture(autouse=True)
	def mock_send_message(self, monkeypatch):
		self.fake_send_message = Mock()
		monkeypatch.setattr(vk, 'send_message', self.fake_send_message)

	def test_da(self):
		assert(self.module.reply(FakeEvent('Да')) == True)
		self.fake_send_message.assert_called_with(100, 'Пизда')

	def test_da_ending(self):
		assert(self.module.reply(FakeEvent('о да!')) == True)
		self.fake_send_message.assert_called_with(100, 'Пизда!')

	def test_da_not_ending(self):
		assert(self.module.reply(FakeEvent('всегда!')) == False)
		self.fake_send_message.assert_not_called()

	def test_mine(self):
		assert(self.module.reply(FakeEvent('наш сервак в майн')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert('178.33.4.203:26126' in calls[0][0][1])

	def test_appeal_net(self):
		assert(self.module.reply(FakeEvent('шпион, нет')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert('Пидора ответ' in calls[0][0][1])

	def test_appeal_wrong(self):
		assert(self.module.reply(FakeEvent('шпио, нет')) == False)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 0)

	def test_often(self):
		assert(self.module.reply(FakeEvent('ахах')) == True)
		assert(self.module.reply(FakeEvent('ахах')) == False)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert(calls[0][0][1] == 'Аахпахпха')

	def test_zaebal(self):
		assert(self.module.reply(FakeEvent('этот бот заебал уже')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)

	def test_zaebal_between(self):
		assert(self.module.reply(FakeEvent('бот уже заебал!')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)

	def test_zaebal_logovenok(self):
		assert(self.module.reply(FakeEvent('заебал логовенок ваш')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)

	def test_empty_message(self):
		assert(self.module.reply(FakeEvent('')) == False)
		self.fake_send_message.assert_not_called()

	def test_F(self):
		assert(self.module.reply(FakeEvent('F')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert(calls[0][0][1] == 'F')

	def test_who(self):
		assert(self.module.reply(FakeEvent('кто лиля?')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)

	def test_multiline(self):
		assert(self.module.reply(FakeEvent('ывы\nваыв\nда')) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
