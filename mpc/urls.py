from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from mpc import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mpc.views.home', name='home'),
    # url(r'^mpc/', include('mpc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    (r'^', include('teams.urls')),
    (r'^', include('members.urls')),
    (r'^', include('attachments.urls')),
    (r'^', include('polls.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
