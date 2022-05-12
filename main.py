import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv

from crawling_site import Usenix

conference_list = ["Usenix", "IEEE Symposium on Security and Privacy", "CCS", "NDSS", "Wisec"]
keyword_list = ["5G", "4G", "LTE", "SIM", "cellular", "Cellular"]

class SlackAPI:
  """
  slack API
  """
  def __init__(self, token):
    self.client = WebClient(token=token)
  # def set_keyword():

  # def get_thread_message():

  def set_block(self, files):
    block = []
    block.append({
      "type" : "section", 
      "text" : {
        "type" : "mrkdwn",
        "text" : "Hello, there are papers for you.\n\n *Please read papers*"
      }
    })
    block.append({
      "type" : "divider"
    })
    for file in files:
      block.append({
        "type" : "section", 
        "text" : {
          "type" : "mrkdwn",
          "text" : "*%s*\n %s" % (file["name"], file["url"])
        }
      })
    self.block = block

  # post message to slack
  def post_message(self, channel_name, files, text=False, message_ts=False):
    # channel
    self.channel_name = channel_name

    # block, thread
    if text == False:
      self.set_block(files)
      self.post_block_message(self)
    else:
      self.post_thread_message(self, text, message_ts)

  def post_block_message(self, message_ts=""):
    try:
      response = self.client.chat_postMessage(
        channel=self.channel_name,
        blocks=self.block,
        text="test"
      )
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      print(e.response["error"])    # str like 'invalid_auth', 'channel_not_found'
      print(e)    

  def post_thread_message(self, text, message_ts=""):
    try:
      response = self.client.chat_postMessage(
        channel=self.channel_name,
        text=text
      )
    except SlackApiError as e:
      # You will get a SlackApiError if "ok" is False
      print(e.response["error"])    # str like 'invalid_auth', 'channel_not_found'
      print(e)

# crawling
year = 22
season = "summer"
usenix = Usenix(year, season)
files = usenix.find_paper()

load_dotenv(verbose=True)

slack_token = os.getenv('SLACK_BOT_TOKEN')
slack = SlackAPI(slack_token)

channel_name = "test"
# text= "Hello from your app! :tada:"
slack.post_message(channel_name, files)