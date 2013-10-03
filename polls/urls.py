from django.conf.urls import patterns, url


urlpatterns = patterns('polls.views',
    # ex: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', 'detail', name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<poll_id>\d+)/results/$', 'results', name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', 'vote', name='vote'),
)