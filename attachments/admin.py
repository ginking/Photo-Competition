from django.contrib import admin

from .models import Attachment


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('photo', )


admin.site.register(Attachment, AttachmentAdmin)