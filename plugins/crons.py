from __future__ import with_statement

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

import codecs

class crons(WillPlugin):


  @periodic(hour='8', minute='00', day_of_week='mon-fri')
  def aperta_triage(self):

    #people = {'Anne': 'EmmaDupin', 'EmmaDupin': 'AngelaMelkisethian', 'AngelaMelkisethian': 'Anne'}
    people = {'Anne':'AngelaMelkisethian', 'AngelaMelkisethian':'Anne'}
    with codecs.open('/home/kbrandt/bot/plugins/yesterday.txt', 'r') as f:
      yesterday = f.readlines()
      yesterday = yesterday[0].strip()
      today = people[yesterday]
    with codecs.open('/home/kbrandt/bot/plugins/yesterday.txt', 'w') as f:
      f.write(today)

    self.say("@{0}, today is your turn to triage support tickets!".format(today), room=self.available_rooms['Publishing Systems Support'])
 
  @periodic(hour='1', minute='00', day_of_week='mon')
  def assess_triage(self):
    review = {'lilcasserole': 'CanadianBacon', 'CanadianBacon': 'ChristopherWiles', 'ChristopherWiles': 'lilcasserole'}
    chasing = {'CanadianBacon': 'lilcasserole', 'lilcasserole': 'CanadianBacon'}
    #ChristopherWiles,lilcasserole
    with codecs.open('/home/kbrandt/bot/plugins/assess.txt', 'r') as f:
      previous = f.read().split(',')
      previous_review = previous[0].strip()
      previous_chase = previous[1].strip()
      current_review = review[previous_review]
      current_chase = chasing[previous_chase]
    with codecs.open('/home/kbrandt/bot/plugins/assess.txt', 'w') as f:
      f.write(','.join([current_review, current_chase]))

    self.say("@{0}, this week is your turn on the Revise report! @{1}, this week is your turn on the Chasing queue!".format(current_review, current_chase), room=self.available_rooms['GEP'])
