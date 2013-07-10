from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import django.http.response

import draftHost.models as models
import draftHost.logic.nfl as nfl
import draftHost.logic.fantasy as fantasy
from draftHost.logic.fantasy import AuthContext as AuthContext

def get_context_or_error(request):
    """Tries to build a AuthContext, raises an error on failure"""
    context = AuthContext(request)
    if context.is_valid():
        return context
     ## TODO - this should probably be a different error
    raise django.http.response.BadHeaderError("invalid auth key")

def draft(request):
    context = get_context_or_error(request)
    return fantasy.JsonFantasyDraft(context.draft).json_response()

def picks(request):
    context = get_context_or_error(request)
    return HttpResponse("picks")

def make_pick(request, pick_id, player_id):
    context = get_context_or_error(request)
    return HttpResponse("picks/make/{p}/player/{who}/"
                        .format(p=pick_id, who=player_id))

def player(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    json_player = nfl.JsonNflPlayer(db_player)
    print "got player and json object {j}".format(j=json_player.json_string())
    return json_player.json_response()

def search(request, query):
    return HttpResponse("search/{q}".format(q=query))

def team_info_id(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    return team_response(team)

def team_info_name(request, name):
    team = {} # TODO
    return team_response(team)

def current_team(request):
    context = get_context_or_error(request)
    return HttpResponse("current team")

def team_response(db_team):
    json_team = fantasy.JsonFantasyTeam(db_team)
    return json_team.json_response()

def register(request):
    return HttpResponse("hello, registration form")
