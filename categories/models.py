from django.db import models

from teams.models import Team

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    involved_teams = models.ManyToManyField(Team)

    def __unicode__(self):
        return unicode(self.category_name)

    def category(self):
        return str(self.category_name)
