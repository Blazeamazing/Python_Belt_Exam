from django.conf.urls import url
from . import views

urlpatterns = [
# here are my routes that render pages
    url(r'^$', views.index, name='landing'),
    # url(r'^success$', views.success, name='success'), this is being removed due to the fact we can use a different route from the secrets app
# here are my routes that have to do with login/logout and registration
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
# here's the route that has to do with friends, + add route parameter: /(?P<id>\d+)
#(?P<id>\d+) means= ?=0-1 occurrence, P=indicates we are going to have a route parameter that matches the <variable>, d+ is at least 1 digit or more. 
    url(r'^add-friend/(?P<id>\d+)$', views.addFriend, name='add-friend'),
    url(r'^remove-friend/(?P<id>\d+)$', views.removeFriend, name='remove-friend'),
    #need a catch all
    url(r'^', views.index, name='default'),
]

#Named Route Notes:
#if I want to use named routes they look like this: name='register'
#   url(r'^register$', views.register, name='register'),
#so now if I want to use this in my html I am going to use a url helper, which looks like this:
#   <form action="{% url 'register' %}"....