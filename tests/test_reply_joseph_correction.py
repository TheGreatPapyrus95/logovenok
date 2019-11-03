import pytest
from unittest.mock import Mock
import time
import vk
from modules.reply_joseph_correction import ReplyJosephCorrection
from tests.fake_event import FakeEvent
import constants


class TestReplyJosephCorrection:
	@pytest.fixture(autouse=True)
	def create_module(self):
		self.module = ReplyJosephCorrection()

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

	def test_did_you_mean(self):
		assert(self.module.reply(FakeEvent('ыдщцф', constants.joseph_id)) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert(calls[0][0][1] == 'Пьянь, ты имел в виду "слова"?')

	def test_no_correction(self):
		assert(self.module.reply(FakeEvent('слова', constants.joseph_id)) == False)
		self.fake_send_message.assert_not_called()

	def test_often(self):
		assert(self.module.reply(FakeEvent('ыдщцф', constants.joseph_id)) == True)
		assert(self.module.reply(FakeEvent('ыдщцф', constants.joseph_id)) == False)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)

	def test_showing_results_for(self):
		assert(self.module.reply(FakeEvent('Я не плнимаю', constants.joseph_id)) == True)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		assert('я не понимаю' in calls[0][0][1])
