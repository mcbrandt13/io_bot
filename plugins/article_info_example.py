__author__ = 'kbrandt'

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import subprocess
from bs4 import BeautifulSoup
import re
import random

qc01_urls = {'pbio':'http://biology-qc01.plosjournals.org:8046/DesktopPlosBiology/article?id=10.1371/journal.',
'pcbi': 'http://compbiol-qc01.plosjournals.org:8046/DesktopPlosCompBiol/article?id=10.1371/journal.',
'pgen': 'http://genetics-qc01.plosjournals.org:8046/DesktopPlosGenetics/article?id=10.1371/journal.',
'pmed': 'http://medicine-qc01.plosjournals.org:8046/DesktopPlosMedicine/article?id=10.1371/journal.',
'pntd': 'http://ntds-qc01.plosjournals.org:8046/DesktopPlosNtds/article?id=10.1371/journal.',
'ppat': 'http://pathogens-qc01.plosjournals.org:8046/DesktopPlosPathogens/article?id=10.1371/journal.',
'pone': 'http://one-qc01.plosjournals.org:8046/DesktopPlosOne/article?id=10.1371/journal.'
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
    cmd = ('echo', '$(mysql -N -s -h hostname -u user ambra -e',
           '"select count(*) from article where doi not rlike', "'image' and date = '$(date +\%Y-\%m-\%d)'", 'and state = 0")')
    word = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE)
    words = word.communicate()[0]
    if words:
      self.say("We've published %s articles so far today." % str(strip_newline(words)), message=message)
    else:
      self.say("barf!", message=message)

  @respond_to("^url")
  def give_url(self, message):
    """url: give me short doi (pone.0293817) and i'll give url, say 'url qc01' for qc01 url"""
    mes = unicode(message)
    print mes
    xml = BeautifulSoup(mes, 'lxml')
    print "from is: " + str(xml.message['from'])
    words = xml.body.string.split(' ')
    regex = '[a-z]{4}\.[0-9]{7}'
    http = 'http://dx.doi.org/10.1371/journal.'
    for word in words:
      if re.match(regex, word):
        if 'qc01' in words:
          self.say("Try: {0}{1}".format(qc01_urls[word[:4]], word), message=message)
        else:
          self.say("Try: {0}{1}".format(http, word), message=message)
