from django.conf.urls import patterns, url
from draftHost import views


urlpatterns = patterns('draftHost.views',
    url(r'^draft/?$', views.draft_key, name='draft'),
    url(r'^draft/(?P<id>\d+)/?$', views.draft_id, name='draft_id'),
    url(r'^picks/?$', views.picks, name='picks'),
    url(r'^pick_player/(?P<player_id>\d+)/?$',
        views.make_pick, name="make_pick"),

    url(r'^player/(?P<uid>\d+)/?$', views.player, name='player'),
    url(r'^player/(?P<uid>\d+)/status/?$',
        views.player_status, name='player_status'),

    # Search views
    url(r'^search/name/(?P<name>[-a-zA-Z]+)/?$',
        views.search, name='search'),
    url(r'^search/name/(?P<name>[-a-zA-Z]+)/pos/(?P<position>\w{1,3})?/?$',
        views.search, name='search_name_pos'),

    url(r'^team/(?P<id>\d+)/?$', views.team_id, name='team_id'),
    url(r'^team/(?P<id>\d+)/players/?$',
        views.fantasy_team_players, name='fantasy_team_players'),
    url(r'^team/(?P<name>.*)/?$', 'team_info_name'),
    url(r'^team/?$', 'current_team'),

    # NFL Data methods
    url(r'^nfl/teams/?$', views.nfl_teams, name='nfl_teams'),
    url(r'^nfl/team/(?P<id>\d+)/players/?$', views.nfl_team_with_players, name='nfl_team_with_players'),
    url(r'^nfl/team/(?P<id>\d+)/?$', 'nfl_team'),
    url(r'^nfl/conferences/?$', views.nfl_conferences, name='nfl_conferences'),
    url(r'^nfl/divisions/?$', views.nfl_divisions, name='nfl_divisions'),
    url(r'^nfl/positions/?$', 'nfl_positions'),
    url(r'^nfl/position/(?P<position>\w{1,3})/?$',
        views.search, name='position_players'),

    # College data methods
    url(r'^colleges/?$', views.colleges, name='colleges'),
    url(r'^college/(?P<id>\d+)/players/?$', views.college_players, name='college_players'),
)
