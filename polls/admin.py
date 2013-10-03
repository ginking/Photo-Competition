from django.contrib import admin

from .models import Poll, Choice


class PollAdmin(admin.ModelAdmin):
    list_display = ('poll', )


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice', )


admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)