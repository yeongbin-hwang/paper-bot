import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv

class SlackAPI:
  """
  slack API
  """
  def __init__(self, token):
    self.client = WebClient(token=token)

  # def set_keyword():

  # def get_thread_message():

  def post_thread_message(self, channel_name, text, message_ts=""):
    try:
      response = self.client.chat_postMessage(
        channel=channel_name,
        text=text
      )
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      print(e.response["error"])    # str like 'invalid_auth', 'channel_not_found'
      print(e)

load_dotenv(verbose=True)

slack_token = os.getenv('SLACK_BOT_TOKEN')
slack = SlackAPI(slack_token)

channel_name = "test"
text= "Hello from your app! :tada:"
slack.post_thread_message(channel_name, text)