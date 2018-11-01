# pyslackhandler
Logging handler to send log entries to slack channel via slack web hook

```
slack_url = 'https://hooks.slack.com/services/...key...'
ch = SlackHandler(webhook_url=slack_url)
ch.setLevel(logging.ERROR)
root.addHandler(ch)
```
