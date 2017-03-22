from django.conf.urls import url
from . import views

app_name = 'coaches' # tell template which app you are working with.

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/$', views.list, name='list'),
    url(r'^connections/$', views.connections, name='connections'),
    url(r'^athlete/(?P<pk>[0-9]+)/$', views.details, name='details'),
]