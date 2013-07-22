from django.conf.urls import patterns, url

from draftHost import views

urlpatterns = patterns('draftHost.views',
    url(r'^draft/?$', views.draft_key, name='draft'),
    url(r'^draft/(?P<id>\d+)/?$', views.draft_id, name='draft_id'),
    url(r'^picks/?$', views.picks, name='picks'),
    url(r'^picks/make/(?P<pick_id>\d+)/player/(?P<player_id>\d+)/?$', 'make_pick'),
    url(r'^player/(?P<uid>.*$)/?$', 'player'),
    url(r'^search/(?P<query>.*)/?$', 'search'),
    url(r'^team/(?P<id>\d+)/?$', views.team_id, name='team_id'),
    url(r'^team/(?P<name>.*)/?$', 'team_info_name'),
    url(r'^team/?$', 'current_team'),
    # HTML views
    url(r'^my_team/(?P<key>[^/]+)/?$', views.my_team, name='my_team'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^/?$', views.draft_page, name='draft_page'),
)
