import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv

from crawling_site import Usenix, NDSS
from basic_types import conference_list, Usenix_years, NDSS_years

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
    # no files
    if (len(files) == 0):
      block.append({
        "type" : "section", 
        "text" : {
          "type" : "mrkdwn",
          "text" : "Hello, there are *no papers* for you.\n\n"
        }
      })
    else:  
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
          "text" : "*%s*\n authors: %s\n%s" % (file["name"], file["authors"], file["url"])
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

load_dotenv(verbose=True)

slack_token = os.getenv('SLACK_BOT_TOKEN')
slack = SlackAPI(slack_token)

channel_name = "test"

# crawling
year = 18
#season = "fall"
for year in [20]:
  usenix = Usenix(year)
  files = usenix.find_all_papers()
  print(files)
  entitys = files.values()
  for entity in entitys:
    if(entity != None and entity != []):
      slack.post_message(channel_name, entity)
# ndss = NDSS(year, season)
# files = ndss.find_paper()
