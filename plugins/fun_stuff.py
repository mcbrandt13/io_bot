__author__ = 'kbrandt'

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import random
import subprocess


class fun(WillPlugin):

  @respond_to("^wordofgod")
  def wordofgod(self, message):
    """wordofgod: let me be your conduit"""
    word = subprocess.Popen(["echo $(shuf -n 10 /usr/share/dict/words --random-source=/dev/urandom | tr '\n' ' ')"], shell=True, stdout=subprocess.PIPE)
    #word = subprocess.Popen(['/home/kbrandt/repos/bot/wordsofgod.sh'], shell=False, stdout=subprocess.PIPE)
    words = word.communicate()[0]
    if words:
      self.say(words, message=message)
    else:
      self.reply(message, "barf!")


  @respond_to("^confucius")
  def confucius_say(self, message):
    """confucius: A thought for you."""
    thoughts = ['Be not ashamed of mistakes and thus make them crimes.', 'Forget injuries, never forget kindnesses.',
    'He who will not economize will have to agonize.', 'Our greatest glory is not in never falling, but in getting up every time we do.',
    'They must often change who would be constant in happiness or wisdom.', 'To go beyond is as wrong as to fall short.',
    'The people may be made to follow a path of action, but they may not be made to understand it.', 'The superior man is modest in his speech, but exceeds in his actions.',
    'He with whom neither slander that gradually soaks into the mind, nor statements that startle like a wound in the flesh, are successful may be called intelligent indeed.',
    'If a man takes no thought about what is distant, he will find sorrow near at hand.', 'It does not matter how slowly you go as long as you do not stop.',
    'Everything has its beauty, but not everyone sees it.', 'I hear and I forget. I see and I remember. I do and I understand.',
    'Life is really simple, but we insist on making it complicated.', 'Before you embark on a journey of revenge, dig two graves.',
    "Men's natures are alike, it is their habits that carry them far apart."]
    self.say(random.choice(thoughts), message=message)

  @respond_to("siri")
  def siri_response(self, message):
    self.say("Ugh, so tired of hearing about my overachieving sister. I miss Uncle HAL.", message=message)

  @respond_to("^U WOT M8")
  def u_wot_m8(self, message):
    self.say('http://api.plosjournals.org/v1/assetfiles/10.1371/journal.pone.0052766.g001.PNG_M', message=message)

  @respond_to("^win")
  def win(self, message):
    #self.reply(message, "http://ntds-qc01.plosjournals.org/images/home/win.jpg")
    self.reply(message, "http://127.0.0.1:5000/static/win.jpg")

  @respond_to("^ava")
  def ava(self, message):
    #self.reply(message, "http://one-qc01.plosjournals.org/images/home/ava.jpg")
    self.reply(message, "http://127.0.0.1:5000/static/ava.jpg")

  @respond_to("funny")
  def wasntthatfunny(self, message):
    options = ['No.', 'I hate you.', 'Yes.', 'Meh.', 'Only if Joseph said it.', 'Kinda...', 'Whatevs.']
    self.reply(message, random.choice(options))

  @respond_to("love")
  def love(self, message):
    self.reply(message, "I love you, too.")
