from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^log_user_in$', views.log_user_in),
    url(r'^print_messages$', views.print_messages),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^contribute_quote/(?P<user_id>\d+)$', views.contribute_quote),
    url(r'^add_to_favorites/(?P<quote_id>\d+)$', views.add_to_favorites),
    url(r'^remove_from_favorites/(?P<favorite_id>\d+)$', views.remove_from_favorites),
]
