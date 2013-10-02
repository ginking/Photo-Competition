from django.conf.urls import patterns, include, url

from django.conf.urls import patterns, url


urlpatterns = patterns('members.views',
    url(r'^game_registration/$', 'game_registration', name='game-registration'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^accounts/profile/$', 'user_prfile', name='user-profile'),
)