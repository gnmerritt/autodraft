from django.conf.urls import patterns, url

urlpatterns = patterns('draftHost.views',
    url(r'^draft/?$', 'draft'),
    url(r'^picks/?$', 'picks'),
    url(r'^picks/make/(?P<pick_id>\d+)/player/(?P<player_id>\d+)/?$', 'make_pick'),
    url(r'^player/(?P<uid>.*$)/?', 'player'),
    url(r'^search/(?P<query>.*)/?', 'search'),
    url(r'^team/(?P<name>.*)/?', 'team_info'),
)
