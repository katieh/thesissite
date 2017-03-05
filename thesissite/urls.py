"""thesissite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

## Login / logout functionality modified from tutorial at:
## https://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^connections/', include('connections.urls', namespace='connections')),
    #url(r'^coaches/', include('coaches.urls', namespace='coaches')),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^athletes/', include('athletes.urls', namespace='athletes')),
    url(r'^admin/', admin.site.urls)
]
