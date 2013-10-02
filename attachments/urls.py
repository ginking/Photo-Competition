from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url


urlpatterns = patterns('attachments.views',
    url(r'^upload_photo/$', 'upload_photo', name='upload-photo'),
)