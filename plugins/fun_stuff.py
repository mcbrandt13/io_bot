__author__ = 'kbrandt'

from bs4 import BeautifulSoup
from selenium import webdriver
from will.plugin import WillPlugin
from will.decorators import respond_to, hear
import datetime
import re
import requests
import random
import subprocess


class fun(WillPlugin):

  @respond_to("^wordofgod")
  def wordofgod(self, message):
    """wordofgod: let me be your conduit"""
    word = subprocess.Popen(["echo $(shuf -n 10 /home/kbrandt/words.txt --random-source=/dev/urandom | tr '\n' ' ')"], shell=True, stdout=subprocess.PIPE)
    #word = subprocess.Popen(['/home/kbrandt/repos/bot/wordsofgod.sh'], shell=False, stdout=subprocess.PIPE)
    words = word.communicate()[0]
    if words:
      self.say(words, message=message)
    else:
      self.reply(message, "barf!")


  @respond_to("^confucius")
  def confucius_say(self, message):
    """confucius: A thought for you."""
    r = requests.get('http://kpbrandt.com/api/confucius')
    self.say(r.json().get('msg'), message=message)

  @respond_to("siri")
  def siri_response(self, message):
    self.say("Ugh, so tired of hearing about my overachieving sister. I miss Uncle HAL.", message=message)

  @respond_to("^U WOT M8")
  def u_wot_m8(self, message):
    self.say('http://kpbrandt.com/static/kpbrandt/images/uwotm8.png', message=message)

  @respond_to("^win")
  def win(self, message):
    self.reply(message, "http://kpbrandt.com/static/kpbrandt/images/win.jpg")

  @respond_to("^ooh")
  def ooh(self, message):
    self.say('http://kpbrandt.com/static/kpbrandt/images/ooh.jpg', message=message)

  @respond_to("^hmm")
  def hmm(self, message):
    self.say('http://kpbrandt.com/static/kpbrandt/images/hmm.png', message=message)

  @hear('^button')
  def button(self, message):
    self.say('http://rs247.pbsrc.com/albums/gg140/theflooper/misc/Historyeraserbutton.jpg~c200', message=message)

  @hear('^no sir')
  def nosir(self, message):
    self.say('http://s2.quickmeme.com/img/66/668f2c316d8211506929d9c3d3a2a2f3d65f130d512411d186520e34d559dce7.jpg', message=message)

  @hear('^random quote')
  def random_quote(self, message):
    """Get a random quote"""
    r = requests.get('http://kpbrandt.com/api/quotes/random')
    x = '"{0}" - {1}'.format(r.json().get('phrase'), r.json().get('author'))
    self.say(x, message=message)

  @respond_to('^reverse (?P<phrase>.*)$')
  def reversed(self, message, phrase):
    """Reverse a string"""
    r = requests.get('http://kpbrandt.com/api/reversed', params={'string': phrase})
    rstring = r.json().get('msg')
    self.say(rstring, message=message)




  @respond_to("funny")
  def wasntthatfunny(self, message):
    mes = unicode(message)
    xml = BeautifulSoup(mes, 'lxml')
    words = xml.message.text
    if 'image me' not in words:
      options = ['No.', 'I hate you.', 'Yes.', 'Meh.', 'Actually, I find it mildly offensive.','Only if Joseph said it.', 'Kinda...', 'Whatevs.']
      self.reply(message, random.choice(options))


  @respond_to("kevinsays")
  def kevinsays(self, message):
    """kevinsays: advice from kevin"""
    advice = ["everything is better as a memory", "nothing's sacred anymore", "lower people's expectations so you may more easily exceed them", "you can make big money if you let yourself make it", "save your energy by remaining indifferent and not liking things by default",]
    self.say(random.choice(advice), message=message)

  @respond_to("^bart")
  def bart_info(self, message):
    """"bart: get some current delay info for BART"""
    r = requests.get('http://kpbrandt.com/api/bart')
    self.say('Bart says: {0}'.format(r.json().get('msg')), message=message)


  @respond_to("^define (?P<search_query>.*)$")
  def define_word(self, message, search_query):
    if len(search_query.split(' ')) > 1:
      self.say('I can only define one word at a time, {0} seems to be more than one word.'.format(search_query), message=message)
    else:
      if search_query == 'merfed':
        def_body = '"merfed":\n to totally mess something up.'
        self.say(def_body, message=message)
      else:
        dictionary_key = '5113d797-0bb9-4e80-a9eb-9cb78604f09c'
        dictionary_query = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{0}?key={1}'.format(search_query, dictionary_key)
        r = requests.get(dictionary_query)
        if r.ok:
          soup = BeautifulSoup(r.text, 'lxml')
          defs = soup.find_all('dt', limit=3)
          et = soup.find_all('et')
          def_body = '"{0}"\n'.format(search_query)
          if not defs:
            def_body += '(shrug)'
          else:
            for e in et:
              def_body += 'Etymology: {0}\n'.format(e.text)
            if defs:
              def_body += 'Three definitions:\n'
              for d in defs:
                def_body += '  {0}\n'.format(d.text)

        thes_key = '80b73d99-109c-45e3-940f-6c524df0cf4b'
        thes_query = 'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/{0}?key={1}'.format(search_query, thes_key)
        r2 = requests.get(thes_query)
        if r2.ok:
          t_soup = BeautifulSoup(r2.text, 'lxml')
          syn = t_soup.find('syn')
          if syn:
            def_body += 'Thesauraus suggestions: {0}'.format(syn.text)
        else:
          def_body = 'Barf, something went awry somewhere.'

        self.say(def_body, message=message)

  @respond_to("image me (?P<search_query>.*)$")
  def image_me(self, message, search_query):
      """image me ___ : Search google images for ___, and post a random one."""
      banned = []#full name like 'Joe Smith'
      if message.sender.name not in banned:
        try:
            url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCihhigU4JWGUKlXg4P1sciZYt2G1o0qJc&cx=014491182948206670424:2ogoc1sxxsa&q={0}&searchType=image&safe=high'.format(search_query)
            r = requests.get(url)
        except Exception:
            count = 0
            pass
        count = r.json().get('queries').get('request')[0].get('count')
        if count > 3:
          n = random.choice([0,1,2])
          x = r.json()['items'][n]
        elif count < 0:
          x = {'link':'None found'}
        else:
            x = {'link': 'Barf!'}
        img_url = x['link']
        self.say("%s" % img_url, message=message)
      else:
        self.say('I am sorry {0}, you are NOT AUTHORIZED to use this function.'.format(message.sender.name),
                 message=message)

  @respond_to('weather (?P<location>.*)$')
  def weather(self, message, location):
    """weather ___ : Provide in format of city, state like 'San Francisco, CA' """
    city, state = location.split(',')
    city = city.strip().replace(' ', '_')
    state = state.strip().upper()
    url = 'http://kpbrandt.com/api/weather'
    r = requests.get(url, params={'city': city, 'state': state})
    if not r.ok:
      self.say('Barf!: {0}'.format(r.text), message=message)
    try:
      r_data = r.json()
      response = 'Location: {0}\nConditions: {1}\nTemp: {2}\nForecast:\n'.format(r_data.get('Location'),
        r_data.get('Conditions'), r_data.get('Temperature'))
      for day, info in r_data.get('Forecast', {}).items():
        response+= '{0}\n'.format(': '.join([day, info]))
    except:
      response = 'you spell that right?'
    self.say(response, message=message)

  @respond_to("^bs")
  def generate_bs(self, message):
    """Generate some corporate bs."""
    r = requests.get('http://kpbrandt.com/api/bs')
    self.say(r.json().get('msg'), message=message)


  @respond_to("^lunch")
  def food_trucks(self, message):
    """Scrape offthegrid.com website to get food trucks for today."""
    self.say('Hold on a sec, checking the offthegrid...', message=message)
    the_date = datetime.datetime.today().strftime('%Y-%-m-%-d')
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(30)
    url = 'https://offthegrid.com/event/vallejo-front/{0}-11am'.format(the_date)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    ul = soup.find('ul', attrs={'class': 'vendors-grid'})
    vendors = []
    for li in ul.find_all('li'):
      name = li.find('header').find('h3').text
      type = li.find('section', attrs={'class': 'food-cat'}).find('span').text
      d = li.find('div', attrs={'class': 'logo-img'}).attrs
      raw = d['style']
      r = re.search('\".+\"', raw)
      img_url = r.group(0).replace('"', '')
      vendors.append({'name': name, 'type': type, 'url': img_url})

    Response =  ''
    for vendor in vendors:
      Response += "{0}: {1}\n{2}\n\n{3}".format(vendor.get('name'),
                                                vendor.get('type'),
                                                vendor.get('url'),
                                                url)

    self.say(Response, message=message)



