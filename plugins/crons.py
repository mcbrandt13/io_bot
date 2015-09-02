from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import subprocess


class crons(WillPlugin):

  @periodic(hour='9', minute='0', day_of_week='mon-fri')
  def wordofgod(self):
    word = subprocess.Popen(["echo $(shuf -n 10 /usr/share/dict/words --random-source=/dev/urandom | tr '\n' ' ')"], shell=True, stdout=subprocess.PIPE)
    words = word.communicate()[0]
    if words:
      self.say("Today's Word of God: %s" % words)
    else:
      self.say("barf!")


  @periodic(hour='10', minute='55', day_of_week='mon-fri')
  def standup(self):
    self.say("I/O Standup up 5 minutes!")

  @periodic(hour='9', minute='55', day_of_week='mon')
  def prioritization(self):
    self.say("I/O Prioritization in 5 minutes!")
