from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import draftHost.logic.objects as objects
import draftHost.models as models

def draft(request):
    return HttpResponse("draft/")

def picks(request):
    return HttpResponse("picks")

def make_pick(request, pick_id, player_id):
    return HttpResponse("picks/make/{p}/player/{who}/"
                        .format(p=pick_id, who=player_id))

def player(request, uid):
    db_player = get_object_or_404(models.NflPlayer, pk=uid)
    json_player = objects.JsonNflPlayer(db_player)
    return json_player.json_response()

def search(request, query):
    return HttpResponse("search/{q}".format(q=query))

def team_info_id(request, id):
    team = get_object_or_404(models.FantasyTeam, pk=id)
    return team_response(team)

def team_info_name(request, name):
    team = {} # TODO
    return team_response(team)

def team_response(db_team):
    json_team = objects.JsonFantasyTeam(db_team)
    return json_team.json_response()

def register(request):
    return HttpResponse("hello, registration form")
