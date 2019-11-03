import pytest
from unittest.mock import Mock
import time
import constants
import vk
from modules.reply_joseph import ReplyJoseph
from tests.fake_event import FakeEvent


class TestReplyJoseph:
	@pytest.fixture(autouse=True)
	def create_module(self):
		self.module = ReplyJoseph()

	@pytest.fixture(autouse=True)
	def mock_send_message(self, monkeypatch):
		self.fake_send_message = Mock()
		monkeypatch.setattr(vk, 'send_message', self.fake_send_message)

	@pytest.fixture(autouse=True)
	def mock_time(self, monkeypatch):
		self.fake_time = Mock()
		self.fake_time.return_value = 99999999
		self.module._last_reply_time = 0
		monkeypatch.setattr(time, 'time', self.fake_time)

	def test_load_quotes(self):
		assert(len(self.module._quotes) > 0)

	def test_not_reply_if_not_joseph(self):
		assert(self.module.reply(FakeEvent('Да', 100500)) == False)

	def test_reply_joseph(self):
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

		reply = self.fake_send_message.call_args[0][1]
		assert(isinstance(reply, str))
		assert(len(reply) > 0)

	def test_send_several_times_in_session(self):
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

	def test_not_send_when_session_closed(self):
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

		self.fake_time.return_value = self.module._last_reply_time + self.module.session_length - 1
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

		self.fake_time.return_value = self.module._last_reply_time + self.module.session_length
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == False)

	def test_send_second_time_after_interval(self):
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

		self.fake_time.return_value = self.module._last_reply_time + self.module.min_interval
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == False)

		self.fake_time.return_value = self.module._last_reply_time + self.module.min_interval + 1
		assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)

	def test_recent_messages(self):
		last_messages = None
		for i in range(100):
			assert(self.module.reply(FakeEvent('Да', constants.joseph_id)) == True)
			reply = self.fake_send_message.call_args[0][1]
			assert(last_messages != reply)
			last_messages = reply
