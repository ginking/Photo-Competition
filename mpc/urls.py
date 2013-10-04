from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from mpc import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    (r'^', include('teams.urls')),
    (r'^', include('members.urls')),
    (r'^', include('attachments.urls')),
    (r'^', include('polls.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
