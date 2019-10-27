# coding=utf-8

import http.client, urllib, datetime

class PushoverSender:
	def __init__(self, user_key, api_key):
		self.user_key = user_key
		self.api_key = api_key

	def send_notification(self, text):
		conn = http.client.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json", urllib.parse.urlencode({
    "token": self.api_key,
    "user": self.user_key,
    "message": text,
  }), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()