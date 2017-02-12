from django.conf.urls import url

from . import views

app_name = 'activities' # tell template which app you are working with.

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'list/$', views.list, name='list'),
    url(r'upload/$', views.UploadView.as_view(), name='upload'), 
    url(r'^(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit')
]