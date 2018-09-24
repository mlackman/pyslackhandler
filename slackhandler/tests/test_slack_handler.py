import unittest
import requests_mock
import threading
from http import server


from slackhandler import handler

class MockSlack:

    called = threading.Event()

    def send(self, msg: str):
        self.called.set()
        self.message = msg

    def wait_for_call(self):
        self.called.wait(3)


class TestSlackLogHandler(unittest.TestCase):


    def test_logging_to_slack(self):
        self.mock_slack = mock_slack = MockSlack()
        def create_mock_slack(*args):
            return mock_slack

        import logging

        root = logging.getLogger()
        slack_handler = handler.SlackHandler(webhook_url='http://localhost:8765/notif', slack_factory=create_mock_slack)
        slack_handler.setLevel(logging.CRITICAL)
        root.addHandler(slack_handler)

        logging.info('jee')
        logging.critical('foobar')

        self._verify_slack_called_with('foobar')

    def _verify_slack_called_with(self, msg: str):
        self.mock_slack.wait_for_call()
        self.assertEqual(msg, self.mock_slack.message)
