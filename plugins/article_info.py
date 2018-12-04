__author__ = 'kbrandt'

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import subprocess
from bs4 import BeautifulSoup
import re
import random
import requests
import datetime
import json

qc01_urls = {'pbio':'http://biology-qc01.plosjournals.org/DesktopPlosBiology/article?id=10.1371/journal.',
'pcbi': 'http://compbiol-qc01.plosjournals.org/DesktopPlosCompBiol/article?id=10.1371/journal.',
'pgen': 'http://genetics-qc01.plosjournals.org/DesktopPlosGenetics/article?id=10.1371/journal.',
'pmed': 'http://medicine-qc01.plosjournals.org/DesktopPlosMedicine/article?id=10.1371/journal.',
'pntd': 'http://ntds-qc01.plosjournals.org/DesktopPlosNtds/article?id=10.1371/journal.',
'ppat': 'http://pathogens-qc01.plosjournals.org/DesktopPlosPathogens/article?id=10.1371/journal.',
'pone': 'http://one-qc01.plosjournals.org/DesktopPlosOne/article?id=10.1371/journal.'
}

def strip_newline(x):
  if x[-1] == '\n':
    return x[:-1]
  else:
    return x

class article_info(WillPlugin):

  @respond_to("^articles")
  def article_count(self, message):
    """articles: Get article count for today."""
    now = datetime.datetime.now()
    d = datetime.datetime.strftime(now, '%Y-%m-%d')
    api_solr_url = 'http://api.plos.org/search?q=publication_date:[{0}T00:00:00Z%20TO%20{0}T23:59:59Z]&rows=1000&id=publication_date&start=0&fq=doc_type:full&wt=json&'.format(d)
    r = requests.get(api_solr_url, headers={'Accept': 'application/json'})
    j = json.loads(r.content)
    count = str(j['response']['numFound'])
    if count:
      self.say("There are %s articles published and indexed in Solr for today." % str(strip_newline(count)), message=message)
    else:
      self.say("barf!", message=message)

  @respond_to("^url")
  def give_url(self, message):
    """url: give me short doi (pone.0293817) and i'll give url, say 'url qc01' for qc01 url"""
    mes = str(message)
    xml = BeautifulSoup(mes, 'lxml')
    words = xml.body.string.split(' ')
    regex = '[a-z]{4}\.[0-9]{7}'
    http = 'http://dx.doi.org/10.1371/journal.'
    for word in words:
      if re.match(regex, word):
        if 'qc01' in words:
          self.say("Try: {0}{1}".format(qc01_urls[word[:4]], word), message=message)
        else:
          self.say("Try: {0}{1}".format(http, word), message=message)
