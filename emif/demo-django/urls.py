from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^sso/$', 'demo-django.views.index', name='sso-index'),
    url(r'^attrs/$', 'demo-django.views.attrs', name='sso-attrs'),
)
