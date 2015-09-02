__author__ = 'kbrandt'

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import subprocess
from bs4 import BeautifulSoup
import re
import requests
import random


class rhino(WillPlugin):

  @respond_to("^fig me (?P<search_query>.*)$")
  def fig_me(self, message, search_query):
    url = 'http://api.plosjournals.org/v1/assetfiles/10.1371/journal.{0}.PNG_M'.format(search_query)
    self.say(url, message=message)

  @respond_to("qc01 fig me (?P<search_query>.*)$")
  def fig_me_qc01(self, message, search_query):
    url = 'http://rhino-qc01.plosjournals.org:8006/api/v1/assetfiles/10.1371/journal.{0}.PNG_M'.format(search_query)
    self.say(url, message=message)

  @respond_to("qc01 ingestibles")
  def qc01_ingestibles(self, message):
    req = requests.get('http://rhino-qc01.plosjournals.org:8006/api/v1/ingestibles')
    if req.ok:
      articles = "Ingestibles are: {0}".format(req.text)
      self.say(articles, message=message)
    else:
      self.say("Barf!")

  @respond_to("^ingestibles")
  def prod_ingestibles(self, message):
    req = requests.get('http://apiambra01.rwc.plos.org/v1/ingestibles/')
    if req.ok:
      articles = "Ingestibles are: {0}".format(req.text)
      self.say(articles, message=message)
    else:
      self.say("Barf!")