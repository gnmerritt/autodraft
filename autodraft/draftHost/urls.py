from django.conf.urls import patterns, url

from draftHost import views

urlpatterns = patterns('draftHost.views',
    url(r'^draft/?$', views.draft_key, name='draft'),
    url(r'^draft/(?P<id>\d+)/?$', views.draft_id, name='draft_id'),
    url(r'^picks/?$', views.picks, name='picks'),
    url(r'^picks/make/(?P<pick_id>\d+)/player/(?P<player_id>\d+)/?$', 'make_pick'),
    url(r'^player/(?P<uid>\d+)/?$', views.player, name='player'),
    url(r'^player/(?P<uid>\d+)/status/?$', 'player_status'),
    url(r'^search/(?P<query>.*)/?$', 'search'),
    url(r'^team/(?P<id>\d+)/?$', views.team_id, name='team_id'),
    url(r'^team/(?P<id>\d+)/players/?$',
        views.fantasy_team_players, name='fantasy_team_players'),
    url(r'^team/(?P<name>.*)/?$', 'team_info_name'),
    url(r'^team/?$', 'current_team'),
    # NFL Data methods
    url(r'^nfl/teams/?$', views.nfl_teams, name='nfl_teams'),
    url(r'^nfl/team/(?P<id>\d+)/players/?$', 'nfl_team_with_players'),
    url(r'^nfl/team/(?P<id>\d+)/?$', 'nfl_team'),
    url(r'^nfl/conferences/?$', views.nfl_conferences, name='nfl_conferences'),
    url(r'^nfl/divisions/?$', views.nfl_divisions, name='nfl_divisions'),
    url(r'^nfl/positions/?$', 'nfl_positions'),
    url(r'^colleges/?$', views.colleges, name='colleges'),
    url(r'^college/(?P<id>\d+)/players/?$', views.college_players, name='college_players'),
    # HTML views
    url(r'^my_team/(?P<key>[^/]+)/?$', views.my_team, name='my_team'),
    url(r'^register/?$', views.register, name='register'),
    url(r'^doc/$', views.documentation, name='documentation'),
    url(r'^/?$', views.draft_page, name='draft_page'),
)
