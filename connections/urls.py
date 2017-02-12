from django.conf.urls import url

from . import views

app_name = 'connections' # tell template which app you are working with.

urlpatterns = [
    url(r'^add/(?P<pk>[0-9]+)/$', views.add, name='add'),
    url(r'^confirm/(?P<pk>[0-9]+)/$', views.confirm, name='confirm'),
    url(r'^reject/(?P<pk>[0-9]+)/$', views.reject, name='reject'),
    url(r'^unfriend/(?P<pk>[0-9]+)/$', views.unfriend, name='unfriend')
]