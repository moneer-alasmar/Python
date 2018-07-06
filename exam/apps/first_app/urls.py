from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^user$', views.user),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^additem$', views.additem),
    url(r'^wishitems/(?P<id>\d+)/$', views.wishitems, name='wish_items'),
    url(r'^join/(?P<id>\d+)/$', views.join, name='join'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete_items'),
]
