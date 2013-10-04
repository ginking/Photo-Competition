from django.conf.urls import patterns, include, url


urlpatterns = patterns('teams.views',
    url(r'^upload_teams/$', 'upload_teams', name='upload-teams'),
)
