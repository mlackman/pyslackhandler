import logging
import threading
import queue
import json

import requests

class Slack:

    def __init__(self, webhook_url: str):
        self.slack_url = webhook_url

    def send(self, msg: str):
        body = {'text': msg}
        requests.post(self.slack_url, headers={'content-type':'application/json'}, data=json.dumps(body))


def create_slack(webhook_url: str):
    return Slack(webhook_url)


class SendingThread(threading.Thread):

    def __init__(self, slack_client):
        super().__init__()
        #self.slack_url = slack_url #'https://hooks.slack.com/services/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'
        self.slack = slack_client
        self._queue = queue.Queue()
        self.daemon = True
        self._stop_thread = False
        self.start()

    def close(self):
        self._stop_thread = True

    def send_message(self, msg: str):
        self._queue.put(msg)

    def run(self):
        while not (self._stop_thread and self._queue.empty()):
            try:
                msg = self._queue.get(timeout=0.1)
                self.slack.send(msg)
            except queue.Empty:
                pass


class SlackHandler(logging.Handler):


    def __init__(self, *args, webhook_url: str, slack_factory: callable=create_slack):
        super().__init__(*args)

        self.addFilter(self._urllib3_filter)
        self._slack = SendingThread(slack_factory(webhook_url))

    def emit(self, record):
        message = self.format(record)
        self._send_to_slack(message)

    def close(self):
        self._slack.close()
        self._slack.join()
        super().close()

    def _send_to_slack(self, msg: str):
        self._slack.send_message(msg)

    def _urllib3_filter(self, record):
        if record.name == 'urllib3.connectionpool':
            return False
        return True
