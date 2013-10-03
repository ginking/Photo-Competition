from django.db import models

from members.models import Member

class Poll(models.Model):
    question = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.question)

    def poll(self):
        return str(self.question)


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='poll_choice')
    choice_member = models.ForeignKey(Member, related_name='choice_member')
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.choice_member)

    def choice(self):
        return str(self.choice_member)