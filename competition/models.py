from django.db import models


from teams.models import Team
from categories.models import Category

class Competition(models.Model):
    competition_name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    involved_teams = models.ManyToManyField(Team)

    def __unicode__(self):
        return unicode(self.competition_name)

    def competition(self):
        return str(self.competition_name)
