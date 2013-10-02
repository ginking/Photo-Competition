from django.db import models

from teams.models import Team
from categories.models import Category
from members.models import Member

class Attachment(models.Model):
    photo_file = models.FileField(upload_to='attachments')
    points = models.IntegerField(default=0)
    team_owner = models.ForeignKey(Team, related_name='attach_team')
    member_owner = models.ForeignKey(Member, related_name='attach_member')
    category = models.ForeignKey(Category, related_name='attach_category')

    def __unicode__(self):
        return unicode(self.file_name)

    def photo(self):
        return format(str(self.file_name).split('/')[-1])


