from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.edit, name='edit'),
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<username>[\w\d]+)/$', views.display, name='display'),
]
