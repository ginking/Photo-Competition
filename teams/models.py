from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
#     active_teams = models.IntegerField(default=0)
#     team_file = models.FileField(default=None, upload_to='media/')

    def __unicode__(self):
        return unicode(self.team_name)

    def update_teams(self):
#         self.active_teams += 1
        self.is_active = True
        self.save()