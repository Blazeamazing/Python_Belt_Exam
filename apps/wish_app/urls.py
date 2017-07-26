from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='success'),
    url(r'^create$', views.create, name='create-wish'),
    url(r'^share$', views.share, name='shared-wish'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
]