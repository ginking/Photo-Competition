from django.contrib import admin

from .models import Competition


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('competition', )


admin.site.register(Competition, CompetitionAdmin)