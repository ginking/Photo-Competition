from django.contrib import admin

from .models import Team


class TeamAdmin(admin.ModelAdmin):
#     list_display = ('team', )
    pass


admin.site.register(Team, TeamAdmin)