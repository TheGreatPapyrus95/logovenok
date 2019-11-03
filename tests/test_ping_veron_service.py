import pytest
import time
from unittest.mock import Mock
import vk
from modules.ping_veron_service import VeronPinger


class TestVeronPinger:
	def setup_class(self):
		self.origin_sleep = time.sleep

	def teardown(self):
		if self.thread:
			self.thread.stop = True

	@pytest.fixture(autouse=True)
	def mock_get_chats(self, monkeypatch):
		self.fake_get_chats = Mock()
		self.fake_get_chats.return_value = {(100, 102)}
		monkeypatch.setattr(vk, 'get_chats', self.fake_get_chats)

	@pytest.fixture(autouse=True)
	def mock_send_message(self, monkeypatch):
		self.fake_send_message = Mock()
		monkeypatch.setattr(vk, 'send_message', self.fake_send_message)

	@pytest.fixture(autouse=True)
	def mock_sleep(self, monkeypatch):
		self.fake_sleep = Mock()
		self.fake_sleep_times = [0]
		self.fake_sleep.side_effect = self.fake_sleep_side_effect
		monkeypatch.setattr(time, 'sleep', self.fake_sleep)

	def fake_sleep_side_effect(self, secs):
		if len(self.fake_sleep_times) == 1:
			time_to_sleep = self.fake_sleep_times[-1]
		else:
			time_to_sleep = self.fake_sleep_times.pop(0)
		self.origin_sleep(time_to_sleep)

	def test_send_once_and_sleep(self):
		self.thread = VeronPinger()
		self.fake_sleep_times = [0, 99999999]

		self.thread.start()

		self.origin_sleep(0.1)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 1)
		call_args = calls[0][0]
		attachments = call_args[2]
		assert(len(attachments) == 1)
		assert('drive.google.com' in attachments[0].url)

	def test_send_several_times(self):
		self.thread = VeronPinger()
		self.fake_sleep_times = [0, 0, 0, 99999999]

		self.thread.start()

		self.origin_sleep(0.1)
		calls = self.fake_send_message.call_args_list
		assert(len(calls) == 2)
		assert('сходка' in calls[0][0][1])
