from django.db import models
# from django.contrib.auth.models import User


class Team(models.Model):
    team_name = models.CharField(max_length=100)
#     team_memebers = models.ManyToManyField(User, related_name='team') # trqbwa da e edin kam mnogo w user
#     active_teams = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
#     team_file = models.FileField(default=None, upload_to='media/')

    def __unicode__(self):
        return unicode(self.team_name)

#     def team(self):
#         return unicode(self.team_name)

    def update_teams(self):
#         self.active_teams += 1
        self.is_active = True
        self.save()