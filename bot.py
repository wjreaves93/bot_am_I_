"""
   COPYRIGHT INFORMATION
   ---------------------

Some code in this file is licensed under the Apache License, Version 2.0.
   http://aws.amazon.com/apache2.0/
"""

from irc.bot import SingleServerIRCBot
from requests import get
import json, urllib.request

with open('./config.json') as data:
   config = json.load(data)

class Bot(SingleServerIRCBot):
   def __init__(self):
      self.HOST = "irc.chat.twitch.tv"
      self.PORT = 6667
      self.USERNAME = config['nickname'].lower()
      self.CLIENT_ID = config['client_id']
      self.TOKEN = config['tmi_token']
      self.CHANNEL = config['channel']

      # Get channel ID
      url = 'https://api.twitch.tv/helix/users?login=will_am_I_'
      header = {'Client-ID': config['client_id'], 'Authorization': 'Bearer ' + config['twitch_token']}
      request = urllib.request.Request(url, headers=header)
      with urllib.request.urlopen(request) as userurl:
         userinfo = json.loads(userurl.read().decode())['data'][0]
      self.CHANNEL_ID = userinfo['id']

      super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

   def on_welcome(self, cxn, event):
      for request in ("membership", "tags", "commands"):
         cxn.cap("REQ", f":twitch.tv/{request}")

      cxn.join(self.CHANNEL)
      self.send_message("Now online.")

   def on_pubmsg(self, cxn, event):
      tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
      user = {"name": tags["display-name"], "id": tags["user-id"]}
      message = event.arguments[0]

      print(f"Message from {user['name']}: {message}")

   def send_message(self, message)
      self.connection.privmsg(self.CHANNEL, message)

if __name__ == "__main__":
   bot = Bot()
   bot.start()