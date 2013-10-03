from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from teams.models import Team
from django.template.defaultfilters import default

class Member(User):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, related_name='team')
    is_leader = models.BooleanField(default=False)
    is_participant = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.username)

    def member(self):
        return str(self.name)

    def update_member(self):
        self.is_participant = True
        self.save()


# class Leader(User):
#     member = models.ForeignKey(Member, related_name='leader_member')
#     team = models.ForeignKey(Team, related_name='leader_team')
#     votes = models.IntegerField(default=0)
# 
#     def votes_update(self):
#         self.votes += 1
#         self.save()

