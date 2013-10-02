from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url


urlpatterns = patterns('teams.views',
    url(r'^upload_teams/$', 'upload_teams', name='upload-teams'),
)