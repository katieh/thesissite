from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'athletes' # tell template which app you are working with.

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'list/$', views.list, name='list'),
    url(r'upload/$', login_required(views.UploadView.as_view()), name='upload'), 
    url(r'^(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^newrun/$', views.edit, name='newrun'),
    url(r'^connections/$', views.connections, name='connections'),
    url(r'^injury/$', views.new_injury, name='new-injury'),
    url(r'^performance/$', views.new_performance, name='new-performance')
]