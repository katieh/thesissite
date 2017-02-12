# modified from:
# https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login'}, name='logout'),
    url(r'^create/$', views.create_account, name='create'),
    url(r'^home/$', views.home, name='home')
]